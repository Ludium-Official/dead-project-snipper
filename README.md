# Overview

The Dead Project Snipper is designed to automatically assess the activity level of blockchain projects and determine if they can be considered "dead" or "inactive". The agent assesses social media scores, github scores, and on-chain activity scores to determine how active the project is building so that the analysis can be further used as a criteria for the grant allocation.

# Problem

According to [Gitcoin’s State of the Web3 Grant Report](https://docs.google.com/document/d/1CFD6ztSh2ggJSO-U3uEea92UVB1cRbvBlA1tfPxLKi8/edit), there are over 1B $USD of grant issued across 5,900 projects in 2023. However, it lacks a standardized and automated measure to assess the activity of the project such that it requires extra effort for validation and the fund may be allocated to the wrong project.

# Solution

Dead Project Snipper offers an automated agent that

1. Collects data from the projects’ social(ex. X), building(ex. Github), and user(ex. onchain transaction) activity and store it on the activity database
2. Calculates the activity score based on the score calculator algorithm for “Dead” and “Active” analysis
3. Reports whether the project is dead or alive with the analysis data to back up the judgement. The report will be stored onchain for further verification

# System Architecture

![Dead Project Snipper.png](https://i.ibb.co/t4HMKjt/Dead-Project-Snipper.png)

### System Flow

The project consist of three main flows, which is coded alphabetically.

* Collect & organize data points: This means figuring out which project is the target for monitoring, and acquiring the project's social/github/wallet address. This part is less about programming; it's more about coordinating with funded projects for information.
* Collect activity data: Once data points are set, we use APIs to monitor and collect activity data in regular cycle.
* Judgement and action: Activity data is ingested to llm-based algorithm. Based on the result score, fact-based reports are created (by llm), actions may be called, and the info is updated to offchain DB & mainnet.

### Details

* Data point / Collector: Github / X Api collecter, Near indexing
* Data Sets for the Metrics: Web3 Grant Funding DB (most likely to be Gitcoin but need discussion)
* Score Calculator: Multipath reasoning algorithm that utilizes LLM-as-a-judge
* Report: Instruction based prompt engineering with RAG on Langchain
* Report UI: Colab with metrics and instructions on how to customize them

# Impact

* Historical Grant Assessment: Check and see whether previous grant projects are still in progress or not
* Grant Project Management: Check the current grant projects to see if their activity should be eligible for the amount
* Grant Criteria Setup: Set up metrics for the least / preferred required activities for the grant recipient

# Roadmap

### Scope

* Phase 1 - Quick Start
    * Objective: Build a testable framework based on minimal data
    * Based on a small set of projects / data set for testing purposes
    * No Web/App UI integration. Only testable results shown on codelab
* Phase 2 - MVP
    * Objective: More dataset / product level UI to start the service adoption
    * Larger dataset for comparison / score calculation
    * Web based UI for datapoint / reporting. Any project can be registered
    * Product ready level for the grant project(ex. Gitcoin, Potlock) integration
* Phase 3 - Expansion
    * Objective: Develop into a project assessment agent
    * In theory, Dead Project Snipper can be generally applied as a project assessment that can not only be applied to Grant Projects outside of Web3, but also any project that requires performance metrics (ex. investment, employment, etc)
    * In order for expansion, it will require multiple data points for the assessment and more developed scoring metrics that befits the purpose of the area of application

# Team

* [Hankeol Jeong/ Bigtide](https://github.com/HangryDev?tab=repositories): The team leader * Led multiple projects including [zkML project](https://devfolio.co/projects/leodevika-b20e) in Aleo * [agent based dev airdrop verifier](https://devfolio.co/projects/gajami-f679) project in. 
* [Sokihoon](https://www.notion.so/1de0b8bdb0754a3d9d1f6e346b878b59?pvs=21):
* AI engineer with R&D and project experiences including image deep learning platform for premium fabric performance prediction, AI based CAD design optimization for shipbuilding, and no code machine learning platform development
* [Ludium](https://docs.google.com/presentation/d/15mmCJ2OYudZY1ncR8kX_eJsq8x8QaTjuOs80ep_TmwE/edit?usp=sharing): Ludium is Web3 builder community with 1,800 + active contributors. It provides opportunities for builders ranging from education, hackathon, to open source contribution based works.

# Questions / Support / Request

* Caveat: For the quick start, SMEs will be seeing Colab UI with “Dead” or “Alive” shown. No Web/App UI for the changes. It is possible to change metrics for the testing purposes
* Project List: The initial project with their data point that would like to be assessed (ex. Potlock grant project that needs assessment)
* Database Collection: Preferred database (ex. All Potlock grant project lists with data point / Gitcoin Grant Project DB)
* Onchain Indexer: Would like to receive recommendation for storing the report onchain / indexer to retrieve project / report information
* Actions after scoring: Is there an existing contract or code? Are there people doing this manually? If so, are there a set process? If there is a code, we could integrate it in the earlier version, making it much cooler
    * Adjust staking allocations or token streaming rates for the project.
        * Update project status in relevant databases or dashboards.
        * Generate alerts for stakeholders or community members.
        * Initiate a review process for projects falling below critical thresholds.
* Service usage : using paid services: cloud provider (aws), openai api, github api, and X apis. Make sure this is not a problem.
* Heads up: collecting and cleaning data might take some money as well. This tends to be underestimated
