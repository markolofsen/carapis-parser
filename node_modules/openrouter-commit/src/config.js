import dotenv from "dotenv";
import path from "path";
import fetch from "node-fetch";
import semver from "semver";
import chalk from "chalk";
import boxen from "boxen";
import { LIBRARY_NAME } from "./constants.js";
import { createRequire } from "module";

const require = createRequire(import.meta.url);
const packageJson = require("../package.json");

export const CONFIG = {
    version: packageJson.version,
    apiKey: process.env.OPENROUTER_API_KEY || "",
    model: process.env.OPENROUTER_MODEL || "deepseek/deepseek-r1"
};

export function loadEnvironment(envPath) {
    dotenv.config({ path: envPath });
}

export async function checkForUpdates() {
    try {
        const response = await fetch(`https://registry.npmjs.org/${LIBRARY_NAME}/latest`);
        const data = await response.json();
        const latestVersion = data.version;

        if (latestVersion && semver.gt(latestVersion, CONFIG.version)) {
            console.log(boxen(
                chalk.yellow.bold("⚠️  Update available!") + "\n" +
                chalk.cyan(`Latest version: v${latestVersion}`) + "\n" +
                chalk.cyan(`Your version: v${CONFIG.version}`) + "\n\n" +
                chalk.white.bold(`Run: npm update -g ${LIBRARY_NAME}`),
                { padding: 1, borderStyle: "round", borderColor: "yellow" }
            ));
        }
    } catch (error) {
        console.warn(chalk.red("⚠️ Failed to check for updates."));
    }
}
