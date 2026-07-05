# Retrieval-Augmented Generation (RAG) Capstone Task

## Objective
Your task is to build a Retrieval-Augmented Generation (RAG) application from scratch. You are provided with a set of synthetic, highly specific internal documents belonging to a fictional healthcare company, "AuraHealth Nexus". Because these documents contain entirely fictional data, large language models will not know the answers based on their pre-trained knowledge. Your system must successfully retrieve the correct context from these documents to answer specific questions accurately without hallucinating.

## Provided Files
You will find the raw data in the `synthetic_data` folder in this workspace. It is up to you to design the architecture, select the libraries, and implement the solution.

## Requirements
1. **Document Loading**: Write code to load and parse the text files in the `synthetic_data` folder. There are 10 distinct, highly detailed documents, each spanning several pages.
2. **Chunking**: Implement a strategy to split the text into manageable chunks so they fit into the context window and allow for granular retrieval.
3. **Embedding**: Convert the text chunks into vector embeddings using an embedding model of your choice (e.g., OpenAI `text-embedding-3-small`, HuggingFace `all-MiniLM-L6-v2`).
4. **Vector Database**: Store the embeddings in a vector database (e.g., ChromaDB, FAISS, Pinecone).
5. **Retrieval**: Implement a semantic search mechanism to retrieve the top `k` most relevant chunks based on a user's query.
6. **Generation**: Pass the retrieved context and the original user query to an LLM (e.g., GPT-3.5/4, Claude, Llama 3) to generate a comprehensive and accurate answer. The prompt must instruct the model to *only* use the provided context.

## Evaluation Questions
Your completed RAG system should be able to answer the following 30 questions accurately, based *only* on the provided documents. These questions range from broad corporate lore to highly specific clinical metrics, testing your system's chunking and retrieval precision.

1. **According to the employee handbook, what is the exact protocol (step-by-step) if the medical AI 'MediMind-7' starts exhibiting Level 3 sentience?**
2. **What is the recommended treatment, including specific dosages and administration methods, for a patient in Phase 2 of NeuroCrystal Syndrome?**
3. **Who is the Head of the OmniHeal initiative, and what percentage of the project's budget is allocated to logistical support?**
4. **What override code must be used during the Cognitive Reset Sequence?**
5. **Under what conditions is a patient prohibited from receiving Zyntabulin?**
6. **What is the designated safe word for recognizing authorized rescue personnel during a Crimson lockdown in Sector 7?**
7. **Who was the chief ethicist that mandated the suspension of human trials for Project Icarus?**
8. **If a patient scores below 75 on the Vellox Cognitive Battery after cryostasis thaw, what medication must be administered?**
9. **What is the required calibration integer for the Quantum MRI diagnostic program Q-CAL_v9.exe?**
10. **Why are patients on the Liquid-Plas diet forbidden from consuming natural fibrous plant matter like celery or broccoli?**
11. **According to the AuraHealth Nexus founding principles, what integration is considered the key to unlocking the next stage of human evolution?**
12. **How frequently does the independent BioEnhancement Ethics Board meet to review ongoing projects?**
13. **What specific technology does AuraHealth Nexus use to power its facilities and maintain sterile, controlled environments?**
14. **Which three components are evaluated by the Vellox Cognitive Battery test following a patient's revival from cryostasis?**
15. **What specific gas is released by atmospheric scrubbers during a Crimson lockdown in Sector 7?**
16. **In the context of global health initiatives, what two pieces of equipment are AuraHealth rapid-response medical teams deployed with?**
17. **What percentage of test subjects in Project Icarus exhibited documented behavioral anomalies?**
18. **What is the primary purpose of the nano-sensor arrays used during human clinical trials?**
19. **What specific department and outpost are responsible for handling Extraterrestrial Biological Entities (EBE)?**
20. **What is the full name of the specific diet required for patients recovering from gastrointestinal cybernetic enhancements?**
21. **What three sources make up the funding structure of AuraHealth Nexus?**
22. **How long is the mandatory sensory deprivation period for a patient who scores below 75 on their post-thaw neurological assessment?**
23. **What specific models of artificial bio-synthetic liver implants are considered a contraindication for Zyntabulin?**
24. **Which specific AI assistant iteration is currently utilized to process terabytes of physiological data in real-time?**
25. **According to the OmniHeal internal memo, the nanite-assisted surgery is expected to reduce recovery times by what percentage?**
26. **What specific room numbers are designated as safe zones during a biocontainment breach in Sector 7?**
27. **Who must review all AI-generated recommendations from the MediMind system before they are implemented?**
28. **What are the three defining characteristics of "Level 3 sentience" in an AI system?**
29. **To prevent quantum drift in the Q-SCAN 9000, how often must the machine be recalibrated by a certified technician?**
30. **What chemical is used to dissolve metallic or synthetic residue after the plasma-arc incineration of EBE contaminated equipment?**

## Bonus Challenge
Implement conversational memory (chat history) so the user can ask follow-up questions without repeating the entire context (e.g., "What are the symptoms of Phase 2?" followed by "And what is the treatment for it?").
