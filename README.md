# Stock Management Assistant

## Overview

The goal is to develop a POC (Proof of Concept) that demonstrates the ability to design an architecture with Agentic AI and Multi-tenancy in a SaaS environment.

The solution is an **Intelligent Stock Management Assistant**. The Assistant should allow users to query the store's inventory in a conversational manner and also trigger restocking actions when inventory falls below minimum levels.

## Scope and Limitations

This POC focuses on demonstrating architecture, orchestration, and multi-tenancy, without covering aspects such as observability, advanced security, and large-scale scalability. The full complexity related to LLM models was also not applied, as the focus was primarily on architecture.

## How to Run

Requirements:
- Python >= 3.9 installed
- Docker
- Postgres >= 14 (optional if running without Docker)

The recommended way to run is through Docker Compose, as it is easier, more practical, and already ensures automatic database initialization and populates tables with predefined content for testing.

1. Clone the repository:
```
    git clone https://github.com/julionog96/stock-management-assistant.git
```

2. Run Docker Compose:
```
    docker compose up --build
```

Optional - Running without Docker:

If you wish to run manually, you can follow the step-by-step instructions below. This mode requires a PostgreSQL database running locally.

1. In the cloned project directory, create a virtual environment:
```
python -m venv .venv
```
Or
```
python3 -m venv .venv
```

2. Now, you need to create the database manually.
Example using psql:
```
CREATE DATABASE stock_db;
CREATE USER stock_user WITH PASSWORD 'stock_pass';
GRANT ALL PRIVILEGES ON DATABASE stock_db TO stock_user;
```

3. Create a .env file with the environment variable:
```
DATABASE_URL=postgresql+psycopg2://stock_user:stock_pass@localhost:5432/stock_db
```

4. Activate the venv and install dependencies

On Linux/MacOS:
```
source .venv/bin/activate
```

On Windows:
```
.venv/bin/activate
```

Now, to install dependencies:
```
pip install -r requirements.txt
```

5. Run the database seeding script
This step is mandatory to have the tables.
```
python -m app.scripts.seed_data
```

6. Run the application:
```
uvicorn app.main:app
```

7. For testing purposes, you can run the stock monitoring job:
```
python -m app.jobs.stock_monitor_job
```

Some notes:

The scheduled job is being represented by an executable script that can be triggered manually. In production, this job could be scheduled via a scheduler (e.g., cron, Celery Beat, Cloud Scheduler) or replaced by an event-driven architecture.

**Authentication and tenant context**
For POC purposes, authentication was kept intentionally simple, using headers for tenant identification. The goal is to demonstrate how a tenant's context is resolved and propagated throughout the entire application. This mechanism ensures that all application flows are tenant-aware.
In a production environment, this could be replaced with something more robust like JWT, OAuth, etc.

## How to Test the Application

After running the application, there are several ways to explore and test the features.

### API Documentation (Swagger)

With the API running locally, access the URL:

http://localhost:8000/docs

Through Swagger, you can:
- Test the health check endpoint
- Interact with the conversational flow (chat)
- Query inventory information by tenant
- Manually trigger the stock monitoring job (if applicable)

Currently, authentication is being simulated via headers. To test protected endpoints, use the Header: X-Tenant-Id: <tenant_id>

### Admin Panel

The application also provides an admin panel:

http://localhost:8000/admin

The panel allows you to view created objects (tenants, products, stocks), and you can also insert and modify data manually. It can be useful to facilitate system testing.

Note: Currently, the panel is without authentication in this POC. Since the only purpose of the panel for now is to facilitate exploration and validation of features, authentication was not prioritized.
In a production environment, this panel must be protected by appropriate authentication and authorization mechanisms.

## Architecture

### Functional Requirements

- Users should be able to query the store's inventory through an interface, like a chatbot.
- The system must automatically trigger restocking actions when inventory falls below minimum levels.
- Users can define what the minimum inventory level is.
- The Agent can act proactively as well as receive user inputs.
- The system will be multi-tenant. Each store manager will be a tenant.
- Tenants will have access to the same database, with logical separation of information by tenant.
- Tenants will access the interface through the same domain (address). The interface will know which tenant it is through authentication and context.

### Architecture Components

**Web Interface / Chat:**
User-friendly interface that allows interaction with the system through conversational chat or visual dashboard.

**API Gateway:**
Single entry point that manages authentication, rate limiting, and request routing.

**Backend API (FastAPI):**
Main API developed in FastAPI that orchestrates all system operations, from authentication to business rule processing.

**Agent Orchestrator:**
Responsible for coordinating communication with the LLM and managing conversation and decision context.

**Tool Calling Layer (LLM):**
Layer that integrates with an LLM (Claude/GPT) using tool calling so the AI autonomously decides which actions to take when inventory is low. Note: in the POC code, the LLM's decision-making is simulated, keeping the focus on architecture and orchestration.

**Tool: Check Stock:**
Tool that checks the current inventory status in real-time and returns detailed information.

**Tool: Refill Stock:**
Tool that automatically creates purchase orders with suppliers when restocking is needed.

**Tool: Notify Manager:**
Tool that sends notifications (email, SMS, push) to the manager when human attention is required.

**Scheduled Job Scheduler:**
Executes scheduled tasks periodically, such as recalculating dynamic thresholds and checking inventory levels.

**Stock Monitoring Service:**
Service that continuously monitors inventory levels and compares them with calculated dynamic thresholds.

**Forecast Engine:**
Forecasting engine that uses statistical models (Prophet, ARIMA) to calculate dynamic thresholds based on seasonality and trends.

**Relational Database:**
Stores product data, inventories, sales history, dynamic thresholds, and tenant information.


## Design Decisions

### Dynamic Threshold Calculation

The assistant needs to function in two flows:
- Users can request inventory information from the agent, and the agent will collect recent information to respond to the user (conversational flow)
- The agent needs to know when inventory levels are low and take action based on that (proactive flow)

On this last point, some considerations:
- Inventory will have a minimum limit that is not necessarily fixed.
- The limit can vary according to tenant, product type, specific inventory location, among other variables
- We could program an interface where the user defines their inventory limits, however, we would be wasting the opportunity to use AI and collected data to our advantage. It doesn't make sense to have something so manual when we can optimize and let the end user not worry about certain indicators.

Therefore, it would be interesting to use artificial intelligence or machine learning tools to determine what this minimum limit, this threshold, would be. We will have some elements in our system that can help with this control:

1 - The limit will be data persisted in the database.

2 - The limit will preferably be changed by the system itself in an intelligent way, with the help of predictions.

3 - A time series forecasting tool will be used (e.g., Prophet, statsmodels...) to update minimum limits dynamically.

The reason for choosing a tool other than the LLM itself to make this prediction is that it would be very expensive to use the LLM every time an event is triggered due to a change in inventory. Therefore, the time series forecasting tool "protects" the agent from being called every time. The goal is that the agent is only requested in this case when inventory levels are low, for decision-making.

**Summary:**
    Agent -> Decision-making
    Time series forecasting -> Business-related calculations

### Conversational Flow (on-demand)

The **conversational flow** will be used for querying inventory information. The idea is for store managers to have an interface to query their inventory information in a simple and intuitive way. When asking a question to the chatbot, the agent can query information obtained from a data retrieval layer (RAG) - presented here only conceptually - composed of persisted or collected-on-demand information. If the inventory information for that tenant is old, the agent will make an active query to the service to collect new data.


![Conversational Flow](./docs/stock-conversational-flow.png)

### Proactive Flow (batch / schedule)

Before diving into the details of the proactive flow, we need to understand the application's context. If we consider a large-scale system with thousands of tenants and the need for real-time updates, it makes sense to use an event-driven architecture to handle the case, and we will break down this projection of a SaaS running in production in the market, with multiple clients, later in this document. For now, since this is a POC, working with event-driven architecture might be using something too large for a simple proposal. Therefore, the POC can use scheduled jobs for simpler processes, as will be explained.

The **proactive flow** will be used for inventory restocking. The idea is an integrated system with an agent. This system, in the POC, will have a scheduled job configured to query the database and check the quantity of products in inventory. When retrieving this information, if inventory levels are below the defined limit, it will consult the agent, passing the current situation and also the API tools (functions) that can be used according to each LLM decision, in a tool calling process. The API receives the response with the definition of which function should be executed and how it will be executed.

On the other hand, it is important to define how this limit, this threshold, will be computed. We will use a time series forecasting tool to define this threshold, by tenant, by inventory, by product, etc., depending on the business rules that will be applied. For this, we will use this same scheduled job - which runs at minute or hour intervals - to feed the tool that will forecast time series with current database data. This tool calculates more accurate minimum inventory limit values based on data and statistics. If the value currently in inventory is already below the minimum value, this service will immediately communicate with the AI agent, which will decide what to do.


![Proactive Flow](./docs/stock-proactive-flow.png)


It is important that the interval is not too short so as not to overload the system components. Considering that if the POC eventually becomes a SaaS in a production environment, there will be several agents simultaneously accessing the database to collect this information. An interval that is too short could overload the database, thus creating bottlenecks or requiring an excessive number of instances to be scaled.

Another factor is the cost of the LLM. Free trial LLMs have a usage limit, and paid ones can end up charging a high amount if there is an excessive number of requests in a short period.

A viable option in the application logic would be to use an event-driven architecture. In event-driven architecture, components communicate in a more decoupled way, through topics and queues where messages are "posted" and wait until they are consumed by some other component. This approach is interesting and makes a lot of sense if we think of a SaaS in production, where it is important to scale when necessary and persist messages even if a component fails. The issue is that in a POC, perhaps an API with a simpler scheduled job would be sufficient. A more event-driven system, perhaps with Change Data Capture, where there is an event stream that is processed by workers, could be a good approach in a world where the SaaS is already on the market and being widely used.


## Communication Protocols

This section describes the communication protocols used between different system components, as well as the architectural decisions behind each choice.
The goal in each choice is always to ensure clarity, low coupling, and facilitate future architecture evolution.

### External Communication (Client ↔ API)

Communication between clients (web/chat interface) and the backend application is done via HTTP/REST.

The HTTP protocol was chosen because it is widely adopted, simple to integrate, and suitable for synchronous interactions, such as conversational queries and direct user commands.


### Internal Communication (Application Components)

Within the application, communication between components occurs directly, via method and function calls, respecting the separation of responsibilities between layers (API, services, agent orchestrator, tools).
For the POC, the idea was to have direct in-memory communication, avoiding unnecessary complexity. In a production scenario, some of these components could communicate through messaging or events.


### Communication with the AI Agent

Communication with the AI agent follows the tool calling pattern, where the agent receives a structured context containing tenant information, system state, and an explicit set of available tools.
It is important to note that the agent does not execute business logic directly; it returns a structured decision indicating which tool should be used and with what parameters. The actual execution of these actions remains under the API's responsibility.

In the POC, the LLM's behavior is simulated, keeping the focus on the architecture and orchestration of the decision flow. A natural evolution would involve evaluating which market LLMs would best fit the context of the operation that the system encompasses, as well as cost issues, among others.

### Evolution to MCP (conceptual)

The Agent Orchestrator was designed to allow future adoption of the Model Context Protocol (MCP), which standardizes the exchange of context, tools, and messages between language models and applications.
Although MCP is not implemented in this POC, the clear separation of context, tools, and decisions allows the agent to be easily adapted to an environment compatible with this protocol.

## Troubleshooting

### Permission Issues When Running Docker on Linux / WSL

In some Linux or WSL environments, permission errors may occur when trying to run Docker commands. Example error:

```
permission denied while trying to connect to the Docker daemon socket
```

In this case, two common solutions would be:

- Run the command with sudo:
  sudo docker compose up --build

- Or add the user to the docker group (requires logout/login):
  sudo usermod -aG docker $USER
