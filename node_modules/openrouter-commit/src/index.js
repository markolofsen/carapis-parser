#!/usr/bin/env node

import path from "path";
import { fileURLToPath } from "url";
import prompts from "prompts";
import chalk from "chalk";
import figlet from "figlet";
import boxen from "boxen";
import { fetchGitStatus, commitAndPush } from "./git.js";
import { checkForUpdates, loadEnvironment,CONFIG } from "./config.js";
import { generateCommitMessage } from "./ai.js";
import { LIBRARY_NAME } from "./constants.js";

const __filename = fileURLToPath(import.meta.url);
const args = process.argv.slice(2);

// 🚀 Ensure '-run' flag is present
if (!args.includes("-run")) {
    console.log(chalk.red.bold(`\nUsage: npx ${LIBRARY_NAME} -run [--env-path <path>]`));
    process.exit(1);
}

// 🛑 Flag to track interruptions
let processInterrupted = false;

// 🔥 Handle process termination signals (Ctrl+C, Ctrl+Break, etc.)
function handleExit(signal) {
    if (!processInterrupted) {
        processInterrupted = true;
        console.log(chalk.red(`\n🚨 Process interrupted with ${signal}. No commit was made.`));
        process.exit(1);
    }
}
process.on("SIGINT", handleExit);
process.on("SIGTERM", handleExit);

// 🎨 Display header
console.log(chalk.cyan(figlet.textSync(LIBRARY_NAME, { horizontalLayout: "fitted" })));

await checkForUpdates();
const envPath = path.resolve(process.cwd(), ".env.openrouter");
loadEnvironment(envPath);

// ✅ Custom prompt handler to prevent commits on ESC
const promptOptions = {
    onCancel: () => {
        console.log(chalk.red("❌ Operation cancelled. No commit was made."));
        process.exit(1);
    },
};

// 🔍 Fetch changed files
const changedFiles = await fetchGitStatus();
if (!changedFiles.length) process.exit(0);

// 🔹 Use `let` so `action` can be reassigned if needed
let { action } = await prompts(
    {
        type: "select",
        name: "action",
        message: "What would you like to do?",
        choices: [
            { title: "✅ Use AI commit", value: "use" },
            { title: "📝 Enter custom commit", value: "custom" },
            { title: "🚪 Exit", value: "exit" },
        ],
    },
    promptOptions
);

if (processInterrupted) process.exit(1); // Prevent further execution if interrupted

if (action === "exit") {
    console.log(chalk.red("❌ Commit aborted."));
    process.exit(0);
}

let commitMessage = "";

if (action === "use") {
    console.log(chalk.cyan(`🤖 Model: ${CONFIG.model}`));

    commitMessage = await generateCommitMessage("", changedFiles);

    if (processInterrupted) process.exit(1); // Check again if interrupted

    if (!commitMessage || commitMessage.trim().length === 0) {
        console.log(chalk.red("❌ AI failed to generate a commit message. Switching to manual entry."));
        action = "custom";
    } else {
        console.log(
            chalk.blue("\n💡 Suggested Commit Message:\n"),
            boxen(chalk.green.bold(commitMessage), { padding: 1, borderStyle: "round", borderColor: "cyan" })
        );

        // 🔥 **Confirm the suggested commit message**
        const { confirmCommit } = await prompts(
            {
                type: "confirm",
                name: "confirmCommit",
                message: "Do you want to use this commit message?",
                initial: true,
            },
            promptOptions
        );

        if (processInterrupted) process.exit(1); // Ensure interruptions prevent further execution

        if (!confirmCommit) {
            console.log(chalk.yellow("✏️ You chose to enter a custom commit message."));
            action = "custom";
        }
    }
}

if (action === "custom") {
    const { customMessage } = await prompts(
        {
            type: "text",
            name: "customMessage",
            message: "Enter your custom commit message:",
        },
        promptOptions
    );

    if (processInterrupted) process.exit(1); // Prevent commit on interruption

    commitMessage = customMessage && customMessage.trim().length > 0 ? customMessage : "Manual commit message.";
}

if (processInterrupted) {
    console.log(chalk.red("❌ Commit aborted."));
    process.exit(0);
}

// 🚀 Push commit with final message
commitAndPush(commitMessage);
