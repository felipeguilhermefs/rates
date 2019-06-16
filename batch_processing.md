# Batch processing question

There is some strategies that could be used in order to design the system,
but they may vary according to requirements:

* By what means the system would receive those big batches?
    * HTTP POST API
    * Message Broker
    * HTTP File Upload
    * FTP Server
* Assuming HTTP (POST or Upload) may I process it asynchronously?
* Can other middlewares be used, like a Message Broker (RabbitMQ, Apache Kafka)?

### Architecture

* The service itself would be stateless.
    * All state would live in the database or in a caching middleware (like Redis or Memcached)
    * We could spin up more instances of the service if needed be.
* Database tables that has historical data, would be partitioned by time.
    * Like "prices" table receives data that refers to a day, it could be partitioned monthly,
    * It ensures that the query performance does not degrades as time passes.
* Would deploy in containers to scale down and up easily
* **Asynchronous Design (Event Driven - 1st Option)**
    * As data is received a worker service would divide the data in smaller pieces and send it to a Message Broker.
    * We would have other (or even the same) worker service listening the Message Broker and processing the smaller pieces of data.
    * The data that could not be processed should be sent to a dead letter queue, for later analysis or reprocessing.
* **Synchronous Design (Fork Join - 2nd Option)**
    * As data is received a manager service would divide the data in smaller pieces and send it to multiple workers (threads, process or services).
    * The workers should process the data and send the 'OK' back to the manager that is waiting.
    * After every worker send its response, the manager can respond the API back with a detailed response, or resend some failed pieces.
* **Asynchronous Design (Deferred Processing - 3rd Option)**
    * As data is received a worker service store the raw data in a persistence layer (file, database, etc).
    * An scheduled job in a worker service would acquire small pieces of the data and process.