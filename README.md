# Syntax_GenAI
## Demo project 

### How to Start and Use Application
Instructions to setup (assumes MacOS)

1. Go to root folder in your terminal
2. Create virtual environment: python3 -m venv gen_ai_venv
3. Activate environment: source gen_ai_venv/bin/activate
4. Install dependences: pip install -r requirements.txt 
5. Run: python 


### The complex problem addressed

How can we provide investment professional subscribers the ability to predict stock market 
drawdowns using GenAI and financial data before they happen so they can protect
their clients' porfolios?

### GenAI frameworks and tools used and the rationale

I used the GenAI tool, DIY, for this demo due to its customization capabilities in handling various datasets,
low overhead as large data and calculations are time intensive, and well-defined tasks like generating insights from financial signals

• Trading models require large amounts of data and processing power for the signal calculations

• I need to directly manage the flow of my specific data (like CSV files and PostgreSQL data) into the AI model without needing to adhere to the structure of a framework

• You avoid the overhead that some frameworks add, allowing you to streamline your code to handle only the essential steps—loading, refining, processing, and feeding data to the model.

### Architecture and Workflow of the Application
• 


Key challenges faced, particularly in terms of integration and advanced functionality, and how they were
overcome:

### Challenges: 
• Generating tradeable signals from financial data is extremely difficult as markets are efficient

• Generating tradeable signals that can be repeatable is even harder

• Understand the limitations of AI. It can NOT predict the future, it can only uncover patterns from history given enough data

• What are the appropriate trading signal(s) such that GenAI tools can uncover patterns (e.g.,
feeding generic closing prices to models may have worked 15 years ago but not in today's market dynamics)

• Understand where in the process GenAI tools are best used. In my opinion, it is in uncovering patterns that are not easily
identifiable to the human eye or through simple statistical processes.

### Solutions:

• Rely on existing academic publications in physics, mathematics, statistics and quantitative finance
to generate reliable trading signals

• Lots of experimentation to determine most relevant prompts that provide the most meaningful feedback to a subscriber/user

• 


Business opportunity:

• Existing services charge up US$700/mo/subscriber to provide meaningful trading signals from data
(e.g., https://squeezemetrics.com/monitor/dix)