# Diogo Soares

**Senior Software Engineer**

Porto, Portugal | +351 916 752 957 | diogo103@gmail.com | [github.com/drsoares](https://github.com/drsoares) | [linkedin.com/in/drcsoares](https://www.linkedin.com/in/drcsoares)

---

## Profile

Senior backend engineer with 13+ years building distributed systems across regulated fintech, e-commerce, and one of the world's largest sports betting platforms. Specialised in event-driven architectures (Kafka, Storm), modernizing legacy systems into resilient microservices, and engineering for scale and reliability — from sub-second market pricing pipelines to RUM platforms ingesting ~100k samples/second. Hands-on across the full stack of production ownership: design, performance tuning, observability, and cross-team troubleshooting on Kubernetes-based AWS and GCP environments.

---

## Experience

### Teya — *Senior Software Engineer* `Jan 2025 – Present`

Senior engineer on the Product Shared Services team, delivering services that power the regulated customer onboarding journey across KYC, identity and document verification, AML/risk checks, merchant provisioning, and external integrations with banks, providers, and regulators.

Key contributor to the design and delivery of a new merchant/account provisioning service designed from scratch, orchestrating downstream onboarding steps and external integrations under strict regulatory and auditability requirements.
Regular participant in performance and chaos engineering Game Days, stress-testing services to identify breaking points, hardening monitoring and observability, and right-sizing infrastructure — including downgrading database tiers and tuning CPU and resource consumption to cut AWS spend without impacting reliability.
Collaborated across multiple teams on platform-level initiatives, gaining broad exposure to the company's systems landscape and acting as a connector between domains.
Developed and evolved services in a heavily event-driven environment using Java, Go, Spring Boot, Kafka, and Avro on AWS-managed Kubernetes, with PostgreSQL as the primary store.

Tech: Java 25, Go, Spring Boot, Maven, PostgreSQL, Kafka, Avro, Docker, Kubernetes, AWS

### Five9 — *Senior Software Engineer* `Jan 2023 – Jan 2025`

Contributed to an internal IaC-style platform tool that provisioned dedicated GCP infrastructure per customer — BigQuery tables, Pub/Sub topics, and Datastore instances — driven by config templates as part of the customer onboarding flow.

Led an end-to-end refactor of the provisioning tool, untangling a legacy codebase that had become a recurring source of incidents and a bottleneck for onboarding new customers — significantly reducing incident frequency and improving provisioning reliability and performance.
Turned ad-hoc per-customer setup into a repeatable, config-driven workflow, making onboarding new customers faster and safer.
Owned the service end-to-end including production support, observability, and reliability of the provisioning pipeline across the GCP stack.

Tech: Java 17, Spring Boot, Gradle, GCP (GKE, Datastore, BigQuery, Pub/Sub)

### Wayfair — *Senior Software Engineer* `Mar 2022 – Jan 2023`

Hired as a Java specialist to help extract product catalog and search/discovery functionality out of a large PHP monolith into Java microservices, incrementally decoupling Catalog domains and improving scalability.

Key contributor to the design of new Java microservices owning product listing and search/discovery flows, applying strangler-fig patterns to incrementally cut traffic over from the PHP monolith without disrupting downstream consumers.
Operated in a high-traffic e-commerce surface where catalog and search reliability directly impact customer-facing browsing and conversion.

Tech: Java 11, Spring Boot, SQL Server, GCP (GKE, BigQuery)

### Blip.pt (Flutter Group) — *Senior Site Reliability Engineer* `Nov 2019 – Feb 2022`

Part of the SRE team supporting one of the largest sports betting platforms in the world, focusing on observability, performance, and infrastructure tooling.

Designed and developed a Real User Monitoring (RUM) platform from scratch, ingesting up to ~100k samples per second at peak, that gave the entire company first-time visibility into page render times, page loads, and mobile request performance — broken down by device model and network conditions — enabling product and engineering teams to act on real user experience issues.
Drove the company-wide adoption of distributed tracing with OpenTracing and Jaeger, working hands-on with platform teams to instrument their services.
Contributed to i2, the company's internal IaC framework running on top of OpenStack on bare metal, helping evolve the framework used to provision and manage infrastructure across the platform.
Authored custom metric agents and acted as a go-to engineer for cross-team troubleshooting — diagnosing network and connectivity issues, performance bottlenecks, memory/CPU resource problems, and gaps in trace coverage across complex service flows.

Tech: Java 8, Go, Python, JavaScript, HBase, Cassandra, OpenStack, GCP, OpenTSDB, Grafana, Jaeger

### Blip.pt (Flutter Group) — *Backend Developer → Senior Backend Developer* `jan 2015 – Nov 2019`

Spent nearly 5 years on the backend platform powering one of the world's largest sports betting operations, progressing from Backend Developer to Senior Backend Developer through two major modernization phases.

Joined during a major platform modernization effort, decomposing monolithic services into fine-grained microservices. Laid the groundwork for the event-driven architecture that would later replace the synchronous pipeline by introducing Kafka and distributed caching to improve throughput and resilience.
Key contributor to the design of the next-generation market management pipeline, re-architecting it from a synchronous chain of services into an event-driven stream-processing platform powered by Kafka and Apache Storm.
The new platform ingested live game incidents and risk-management events from 4 feed providers, reflecting changes in real-time on odds pricing and market lifecycle states (active, suspended, settled) across pre-match, live in-play, risk/trading, and settlement flows — with sub-second end-to-end latency.
Eliminated backpressure bottlenecks and enabled horizontal scaling, with the architecture designed to handle millions of events per second as the catalogue of sports, events, and markets grew.

Tech: Java 7/8, Scala, Spring, Maven, Apache Storm, Kafka, Cassandra, ZooKeeper, RabbitMQ, ActiveMQ, Redis, Hazelcast, Couchbase, MySQL, Protobuf

### grupo@work — *Backend Developer* `Dec 2013 – Dec 2014`

Part of a small core team that delivered a greenfield ticketing and bar-inventory management solution for one of Portugal's largest cinema-theatre groups, supporting in-person, mobile, and web channels. Delivered to production and rolled out across multiple venues.

Tech: Java 7, Maven, Spring, PostgreSQL, Apache Tapestry, Liquibase, SymmetricDS, Swing

### PT Inovação — *Junior Backend Developer* `Feb 2013 – Dec 2013`

Contributed to multiple products serving mobile telecommunications clients, gaining early-career experience across diverse Java frameworks and database technologies.

Tech: Java 6, Scala, Maven, Play Framework, Struts 2, JBoss, Netty, Oracle 11g

---

## Education

### Universidade de Aveiro `2006 – 2012`

Master's in Computer Science Engineering and Telematics

---

## Certifications & Courses

- [Functional Programming Principles in Scala](https://www.coursera.org/account/accomplishments/certificate/SJX5MJ4MKL) — Coursera
- [Kotlin for Java Developers](https://www.coursera.org/account/accomplishments/certificate/6ZN3PQY5UUGZ) — Coursera
- [M101J: MongoDB for Java Developers](https://university.mongodb.com/course_completion/9740179520cf4c129c25f6e63e94a285) — MongoDB, Inc.