# Syntax_GenAI
## Demo project 

This is a demo project, a proof of concept, to showcase the combination of trading signals and GenAI tools
together can generate superior market information for an investor.


### How to Start and Use Application
Setup (assumes MacOS)

1. Go to root folder in your terminal
2. Create virtual environment: python3 -m venv gen_ai_venv
3. Activate environment: source gen_ai_venv/bin/activate
4. Install dependences: pip install -r requirements.txt 
5. Run: python main.py
6. Interact with the agent by advising it what date you are referencing followed by 
what it's market prediction is (e.g., today is July 30, 2024, what do you expect of markets in the near term?)

### The Problem Statement

How can we provide investment professional subscribers the ability to predict stock market 
drawdowns using GenAI and financial data before it happens to protect clients' porfolios?

### GenAI Frameworks and Tools Used and Rationale

I used the GenAI tool, DIY, for this demo due to:

• Customization capabilities in handling various datasets,

• Low overhead as large data sets and heavy calculations are already time and resource intensive,
and it allows one to streamline code to handle only the essential steps—loading, refining, processing, and feeding data to the model.

• Suitability for well-defined tasks like generating insights from financial signals.

• The need to directly manage the flow of specific data sets (like CSV files and PostgreSQL data) into the AI model without 
needing to adhere to the structure of a rigorous framework.

I used the Chat Completions API functionality as it is designed to handle conversational prompts, allowing for multi-turn interactions
where each response can build on prior context. This functionality is essential for responding to user queries about market insights 
(e.g., “How likely will the market correct in the next few weeks?”) and for simulating advisor-like behavior in interpreting financial data trends.

As a next step, I would like to experiment with Langchain for multi-step queries. This could be beneficial for extended analysis 
in financial forecasting or for creating a sequence of GenAI model prompts that connect various data insights.

### Architecture and Workflow of the Application
Sample data used as input to GenAI tool. The blue line is the signal - the entropic indicator. The green line is the price of the S&P500 index price.
The red line is a proxy of how expensive hedging is in the market.
![Screenshot of the Training Data and Ground Truth](./entropy_training_data.png)

Architecture of how data is obtained, transformed/processed, and transferred into the GenAI tool.
![Architecture Diagram of Data Flow and Processing](./Syntax_GenAI.png)


### Key Challenges

#### Challenges: 
• Generating tradeable signals from financial data is extremely difficult

• Generating tradeable signals that can be repeatable is even harder

• Understand the limitations of AI. It can NOT predict the future, it can only uncover patterns from history given the data is high quality

• What are the appropriate trading signal(s) such that GenAI tools can uncover patterns (e.g.,
feeding generic closing prices to models may have worked 15 years ago but not in today's market dynamics)

• Understanding where in the process GenAI tools are best used. In my opinion, the best use is in uncovering patterns that are not easily
identifiable to the human eye or through simple statistical processes.

• Challenges in setting up the appropriate prompt and narrowing the scope of the output of the GenAI model so that
the most meaningful output is produced consistently.

• Experienced challenges in parameter use including which model, temperature=0.2, and max_tokens=250 to balance cost with conciseness
and meaningful output.

#### Solutions:

• Relied on existing academic publications in physics, mathematics, statistics and quantitative finance
to generate reliable and consistent trading signals. This was significant time investment and difficult to replicate - I believe this is
a large value add and creates the highest quality input data for the GenAI model. 

• Required significant experimentation to determine the best model to use. Eventually I settled on gpt-4o-mini as it was most cost-effective
and still generated meaningful output consistently. 

• Experimentaion also led to a temperature parameter of 0.2 to ensure reliable, consistent answers with less variability. 
With financial data, predictability, consistency and accuracy are critical at a tradeoff for more creative answers seen in higher parameter values.  

### Business opportunity:

• Existing services charge up US$700/mo/subscriber to provide meaningful trading signals from data but they are not interactive and you can't ask questions
(e.g., https://squeezemetrics.com/monitor/dix)

### System Dependencies

To install this project, make sure you have the following system libraries:

- **freetype**: Required by matplotlib for font rendering
- **libpng**: Required by matplotlib for handling PNG images
- **pkg-config**: Helps pip locate the above libraries during installation

#### Installing System Libraries on macOS
You can install these libraries using Homebrew:

```bash
brew install freetype libpng pkg-config