# Paolo Gallo

Head of Decision Intelligence in the intelligence and defence technology sector. 25+ years building AI and data products from zero to production: knowledge graphs, NLP/NLU, multi-agent systems, distributed computing and human-in-the-loop decision support.

The common thread is 0 to 1: six products taken from a blank page to real users, starting with clinical monitoring software for intensive care in 1996.

[LinkedIn](https://www.linkedin.com/in/paologallo/)

## Lab portfolio

The production systems I have built are proprietary. The repositories below are public reference implementations, written in 2026 on synthetic data, that reconstruct the engineering patterns behind that work. Each one builds, runs a demo and has tests in CI.

| Repository | Stack | What it shows |
|---|---|---|
| [decision-model-lab](https://github.com/pgallo/decision-model-lab) | Python | Decision models, DMN-style decision tables, Monte Carlo, value of information, evidence fusion, applied to life sciences, insurance, banking fraud and intelligence analysis |
| [mcp-hitl](https://github.com/pgallo/mcp-hitl) | Python, TypeScript | Twin MCP servers behind one contract and one conformance suite; human approval policy and hash-chained audit trail |
| [kg-rag-lab](https://github.com/pgallo/kg-rag-lab) | Python | Neuro-symbolic retrieval: RDF knowledge graph, entity linking, hybrid graph and vector retrieval, LLM-as-judge evaluation |
| [actor-council](https://github.com/pgallo/actor-council) | Java 21 | Typed actor runtime written from scratch, multi-agent evidence fusion with supervision and human review |
| [blackboard-rmi](https://github.com/pgallo/blackboard-rmi) | Java 21, RMI | Distributed blackboard system: knowledge sources in separate JVMs, opportunistic control |
| [matchmaker-grid](https://github.com/pgallo/matchmaker-grid) | Python | High-throughput computing: declarative resource ads, symmetric matchmaking, fair-share scheduling, DAG workflows |
| [georesolve-cpp](https://github.com/pgallo/georesolve-cpp) | C++17 | Toponym disambiguation with HMM decoding and KNN context models |
| [wifi-fasthandoff](https://github.com/pgallo/wifi-fasthandoff) | C11, Python | Fast Wi-Fi handoff in driver logic with a learned next-AP predictor, and a content delivery layer that keeps sessions continuous across handoffs |
| [telemetry-orb](https://github.com/pgallo/telemetry-orb) | C++17, CORBA | Real-time telemonitoring over CORBA with push subscriptions and per-subscriber QoS |
| [bedside-link](https://github.com/pgallo/bedside-link) | Object Pascal | Connectivity gateway for intensive-care equipment: protocol drivers, HL7 v2, alarm engine |
| [fleetline](https://github.com/pgallo/fleetline) | C++17, Python | Fleet telematics: C++ stream engine for geofencing and trips, Python service and analytics via pybind11 |
| [casefile-dotnet](https://github.com/pgallo/casefile-dotnet) | C#, .NET 8 | Case management with a from-scratch BM25 search engine, facets and link analysis |
| [kyc-energy-graph](https://github.com/pgallo/kyc-energy-graph) | Python | KYC and AML for energy and utilities: entity resolution across registry and data feeds, ownership graphs, confidence-scored key-person risk |
| [waypoint-android](https://github.com/pgallo/waypoint-android) | Rust, Kotlin | Offline-first Android app with a Rust core shared through UniFFI and CRDT-style sync |

## Timeline

Each lab reconstructs, in 2026 and on synthetic data, an approach I first applied in production or in applied research in the period shown. From 2007 onward every system I built combined AI and machine learning (HMM, KNN, SVM, neural networks) with knowledge graphs.

| Period | Original work | Lab |
|---|---|---|
| 1996 | Connectivity for intensive-care equipment | [bedside-link](https://github.com/pgallo/bedside-link) |
| 2002 | Real-time telemonitoring over CORBA in C++ | [telemetry-orb](https://github.com/pgallo/telemetry-orb) |
| 2003 | Fleet management in C++ and Python | [fleetline](https://github.com/pgallo/fleetline) |
| 2004 to 2005 | Distributed computing experiments with blackboard architectures | [blackboard-rmi](https://github.com/pgallo/blackboard-rmi) |
| 2006 | Grid computing with matchmaking schedulers | [matchmaker-grid](https://github.com/pgallo/matchmaker-grid) |
| 2007 | Geo-disambiguation engine in C++ (HMM, KNN, SVM, neural networks) | [georesolve-cpp](https://github.com/pgallo/georesolve-cpp) |
| 2007 | Fast Wi-Fi handoff adapted inside the driver, with ML next-AP prediction and content continuity for the delivery platform | [wifi-fasthandoff](https://github.com/pgallo/wifi-fasthandoff) |
| 2011 to 2015 | Actor-based multi-agent systems for decision intelligence, with ML and neural network models | [actor-council](https://github.com/pgallo/actor-council) |
| 2014 to 2018 | Case management and semantic search for analysts, with ML and neural network NLP | [casefile-dotnet](https://github.com/pgallo/casefile-dotnet) |
| 2018 | KYC and AML for energy and utilities: entity resolution, ownership graphs, key-person risk, with ML and neural network models | [kyc-energy-graph](https://github.com/pgallo/kyc-energy-graph) |
| 2019 to 2023 | Neuro-symbolic knowledge graphs combining ML, neural networks and symbolic AI; LLM-as-judge evaluation | [kg-rag-lab](https://github.com/pgallo/kg-rag-lab) |
| 2023 to present | MCP, LLM pipelines and human-in-the-loop agents | [mcp-hitl](https://github.com/pgallo/mcp-hitl) |
| 2024 to present | Decision models with ML and neural networks in life sciences, insurance, banking fraud and intelligence | [decision-model-lab](https://github.com/pgallo/decision-model-lab) |
| 2026 | Exploration: Rust domain core shared with an Android UI | [waypoint-android](https://github.com/pgallo/waypoint-android) |

## Capability map

| Capability | Where to look |
|---|---|
| Decision intelligence and decision modelling | decision-model-lab, actor-council |
| KYC, AML and financial crime | kyc-energy-graph, decision-model-lab |
| Entity resolution and ownership graphs | kyc-energy-graph, kg-rag-lab |
| Human-in-the-loop AI, explainability, audit | mcp-hitl, actor-council, decision-model-lab |
| LLM pipelines, RAG, GraphRAG, evaluation | kg-rag-lab, mcp-hitl |
| Knowledge graphs, ontologies, semantic search | kg-rag-lab, casefile-dotnet |
| NLP/NLU and classical ML (HMM, KNN, gradient boosting) | georesolve-cpp, decision-model-lab |
| Multi-agent systems and actor model | actor-council, blackboard-rmi |
| Distributed and grid computing (CORBA, RMI, matchmaking) | telemetry-orb, blackboard-rmi, matchmaker-grid |
| Real-time systems and device integration | bedside-link, telemetry-orb, fleetline, wifi-fasthandoff |
| Wireless networking, driver logic and content delivery | wifi-fasthandoff |
| Geospatial processing | georesolve-cpp, fleetline, waypoint-android |
| Mobile and offline-first sync | waypoint-android |
| APIs and services | casefile-dotnet, fleetline, mcp-hitl |

Languages: Python, C++, C, Java, C#, TypeScript, Object Pascal, Rust, Kotlin.

## Production systems (confidential)

The systems below are proprietary and not public. The drawings are simplified, concept-level blueprints of my own design work. They contain no code, data, customer names or implementation details.

### Decision intelligence fusion platform (2023 to present)
![Decision intelligence fusion platform blueprint](blueprints/bp-01-decision-intelligence-platform.svg)

### Cyber threat intelligence for continuous threat exposure management (2023 to present)
![Cyber threat intelligence for CTEM blueprint](blueprints/bp-02-threat-intelligence-ctem.svg)

### Narrative intelligence
![Narrative intelligence blueprint](blueprints/bp-07-narrative-intelligence.svg)

### Neuro-symbolic life sciences knowledge platform (2019 to 2023)
![Life sciences knowledge platform blueprint](blueprints/bp-03-life-sciences-knowledge-platform.svg)

### Case management and semantic search for analysts (2014 to 2018)
![Analyst case management blueprint](blueprints/bp-04-analyst-case-management.svg)

### Semantic intelligence suite (2007 to 2014)
![Semantic intelligence suite blueprint](blueprints/bp-05-semantic-intelligence-suite.svg)

### Intensive care monitoring system (1996)
![ICU monitoring system blueprint](blueprints/bp-06-icu-monitoring-system.svg)

The drawings are generated by [`tools/blueprint.py`](tools/blueprint.py).
