import fetch from "node-fetch";
import chalk from "chalk";
import { CONFIG } from "./config.js";

export async function generateCommitMessage(diff, changedFiles) {
    console.log(chalk.cyan(`🤖 Generating commit...`));

    try {
        let systemMessage = `
            Generate a concise git commit message.
            Don't include the file names or line numbers.
            Don't include "Commit message" in the response.
            Be concise and clear.
            Add short title and description.
            Don't use markdown, just plain text.

            The following files have changed: ${changedFiles.join(", ")}.
        `;

        // remove extra spaces and newlines
        systemMessage = systemMessage.replace(/\s+/g, " ").trim();
        
        const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
            method: "POST",
            headers: { "Content-Type": "application/json", "Authorization": `Bearer ${process.env.OPENROUTER_API_KEY}` },
            body: JSON.stringify({
                model: CONFIG.model,
                messages: [{ role: "system", content: systemMessage }, { role: "user", content: diff }],
                temperature: 0.7,
            }),
        });

        const data = await response.json();

        console.log(chalk.yellow("📥 OpenRouter API Response:"), JSON.stringify(data, null, 2));

        if (!data.choices || !data.choices[0] || !data.choices[0].message || !data.choices[0].message.content) {
            return null;
        }

        return data.choices[0].message.content.trim();
    } catch (error) {
        console.error(chalk.red("❌ OpenRouter API request failed."), error);
        return null;
    }
}
