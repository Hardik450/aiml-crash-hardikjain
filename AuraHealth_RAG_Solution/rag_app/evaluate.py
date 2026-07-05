import json
import time
from rag_pipeline import RAGPipeline

QUESTIONS = [
    "According to the employee handbook, what is the exact protocol (step-by-step) if the medical AI 'MediMind-7' starts exhibiting Level 3 sentience?",
    "What is the recommended treatment, including specific dosages and administration methods, for a patient in Phase 2 of NeuroCrystal Syndrome?",
    "Who is the Head of the OmniHeal initiative, and what percentage of the project's budget is allocated to logistical support?",
    "What override code must be used during the Cognitive Reset Sequence?",
    "Under what conditions is a patient prohibited from receiving Zyntabulin?",
    "What is the designated safe word for recognizing authorized rescue personnel during a Crimson lockdown in Sector 7?",
    "Who was the chief ethicist that mandated the suspension of human trials for Project Icarus?",
    "If a patient scores below 75 on the Vellox Cognitive Battery after cryostasis thaw, what medication must be administered?",
    "What is the required calibration integer for the Quantum MRI diagnostic program Q-CAL_v9.exe?",
    "Why are patients on the Liquid-Plas diet forbidden from consuming natural fibrous plant matter like celery or broccoli?",
    "According to the AuraHealth Nexus founding principles, what integration is considered the key to unlocking the next stage of human evolution?",
    "How frequently does the independent BioEnhancement Ethics Board meet to review ongoing projects?",
    "What specific technology does AuraHealth Nexus use to power its facilities and maintain sterile, controlled environments?",
    "Which three components are evaluated by the Vellox Cognitive Battery test following a patient's revival from cryostasis?",
    "What specific gas is released by atmospheric scrubbers during a Crimson lockdown in Sector 7?",
    "In the context of global health initiatives, what two pieces of equipment are AuraHealth rapid-response medical teams deployed with?",
    "What percentage of test subjects in Project Icarus exhibited documented behavioral anomalies?",
    "What is the primary purpose of the nano-sensor arrays used during human clinical trials?",
    "What specific department and outpost are responsible for handling Extraterrestrial Biological Entities (EBE)?",
    "What is the full name of the specific diet required for patients recovering from gastrointestinal cybernetic enhancements?",
    "What three sources make up the funding structure of AuraHealth Nexus?",
    "How long is the mandatory sensory deprivation period for a patient who scores below 75 on their post-thaw neurological assessment?",
    "What specific models of artificial bio-synthetic liver implants are considered a contraindication for Zyntabulin?",
    "Which specific AI assistant iteration is currently utilized to process terabytes of physiological data in real-time?",
    "According to the OmniHeal internal memo, the nanite-assisted surgery is expected to reduce recovery times by what percentage?",
    "What specific room numbers are designated as safe zones during a biocontainment breach in Sector 7?",
    "Who must review all AI-generated recommendations from the MediMind system before they are implemented?",
    "What are the three defining characteristics of \"Level 3 sentience\" in an AI system?",
    "To prevent quantum drift in the Q-SCAN 9000, how often must the machine be recalibrated by a certified technician?",
    "What chemical is used to dissolve metallic or synthetic residue after the plasma-arc incineration of EBE contaminated equipment?",
]


def main():
    pipeline = RAGPipeline(top_k=5)
    pipeline.index()

    results = []

    for i, q in enumerate(QUESTIONS, 1):
        retrieved = pipeline.store.search(q, top_k=5)
        answer = pipeline.generator.generate(q, retrieved, history=None)
        
        result = {
            "question_number": i,
            "question": q,
            "top_sources": [c.source for c, _ in retrieved[:3]],
            "answer": answer,
        }
        results.append(result)

        print(f"Q{i}: {q}")
        print(f"Top sources: {result['top_sources']}")
        print(f"A{i}: {answer}\n{'-'*80}")

        if i < len(QUESTIONS):
            time.sleep(10)

    with open("evaluation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("Saved evaluation results to evaluation_results.json")


if __name__ == "__main__":
    main()
