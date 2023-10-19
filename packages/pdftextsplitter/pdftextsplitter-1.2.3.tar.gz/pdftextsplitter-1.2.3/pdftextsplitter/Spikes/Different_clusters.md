# Test with Different Clusters

This test is about how much of a reduction in computational time
can be achieved with a heavier cluster in Azure databricks.

### Test run

the test run was executed with the DocAnalyse_Count-notebook.
This notebook operates on civillian correspondence letters,
stored as text with metadata in the Azure datalake. the notebook
loads the letters and setps up the langchain packages so that
one can ask questions to the documents with ChatGPT. <br />
<br />
In this specific situation, one wants to classify the documents
on topic (asbest in the example). This is done by converting
each letter individually to a Chroma-database using OpenAI Embeddings.
then, we ask a binary question on the topic to each Chroma-object
and count the number of 'yes'-responses. <br />
<br />
The two bottlenecks are the creation of all the Chroma-DB objects
and asking the binary questions (20 in our test).

### Shared Compute Cluster

This is the standard cluster used bij DenI in Azure Databricks.
It is a D4s_v5 type with 16 GB, 4 cores and 5 workers.
* Creating the Chroma-db objects took 1.22 minutes
* Asking the questions took 2.81 minutes.
* The cluster price is 0.21 euro per hour.

### Heavy Cluster

For this test, we used a D32ds_v4 cluster in Azure Databricks.
* Creating the Chroma-db objects took 51 sec.
* Asking the questions took 29 sec.
* The cluster price is 2 euro per hour.

### Conclusions

* Asking the questions benefits significantly more from a heavy cluster
then creating the Chroma-db objects. As such, it is advantageous to
perform all classifications at once so the Chroma's only have to be created once.
* While there certainly is benefit, it is far less then one would expect.
Chroma has 1.43x speed-up and Q&A has 5.8x speed-up. One would expect around 8x speed-up
when scaling from 4 cores, 5 workers to 16 cores, 10 workers.
* The code was not written multi-threaded. We expect this to offer better speed-up.
But then it is not an easy proof-of-concept anymore that can be stored in a notebook.
To do that, we need to actually build a product, not proof-of-concept.
* Multi-threaded offers another major advantage. Especially asking the questions is
somewhat unstable. When we multi-thread, we can easily keep track on which
question failed and then we can try that again. This is much harder serialized and
the unstability problem grows with the number of letters.

<br />

So yes, a heavier cluster offers significant speed-up. But we cannot take truly advantage of that
until we multi-thread the code. An investment certainly worth it, as we also expect a more stable code.

### Final remarks

We also need a better method for installing libraries. Currently the only way is to do pip install
EVERY time the cluster restarts. This is not good enough for actual products.
