import pandas as pd
import faiss
from retrieval.embeddings import model

DATA_FILE = "data/maintenance_records.csv"


def add_feedback_case(
    complaint,
    equipment_type,
    equipment_id,
    location,
    actual_cause,
    actual_resolution,
    actual_cost,
    actual_time,
    urgency="Medium"
):
    df = pd.read_csv(DATA_FILE)

    next_number = len(df) + 1

    new_case = {
        "case_id": f"FEEDBACK-{next_number:04d}",
        "equipment_type": equipment_type,
        "equipment_id": equipment_id,
        "location": location,
        "complaint": complaint,
        "symptoms": complaint,
        "previous_action": "Technician inspection",
        "root_cause": actual_cause,
        "resolution": actual_resolution,
        "cost": actual_cost,
        "repair_time": actual_time,
        "urgency": urgency,
        "technician_notes": "Added from technician feedback",
        "status": "Confirmed"
    }

    new_row = pd.DataFrame([new_case])

    df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    df.to_csv(
        DATA_FILE,
        index=False
    )

    
# Rebuild FAISS index after adding feedback
    from retrieval import embeddings

    embeddings.df = df

    search_texts = df.apply(
        embeddings.create_search_text,
        axis=1
    ).tolist()

    new_embeddings = model.encode(
        search_texts,
        show_progress_bar=False
    )

    embeddings.index = faiss.IndexFlatL2(
        new_embeddings.shape[1]
    )

    embeddings.index.add(
        new_embeddings.astype("float32")
    )
    return new_case