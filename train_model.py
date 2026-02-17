import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors
from config import settings
from ml.features import prepare_training_data, train_tfidf

def main():
    df = pd.read_csv(settings.RAW_DATA_PATH)

    # Prepare data with all fields
    pairs, severities, descriptions, risk_levels, affected_organs, pair_map = prepare_training_data(df)

    # Train TF-IDF
    vectorizer, X = train_tfidf(pairs, max_features=500)

    # Train kNN
    knn = NearestNeighbors(n_neighbors=min(5, len(pairs)), metric='cosine', algorithm='brute')
    knn.fit(X)

    # Save assets
    with open(settings.TFIDF_PATH, 'wb') as f:
        pickle.dump(vectorizer, f)
    with open(settings.KNN_PATH, 'wb') as f:
        pickle.dump(knn, f)
    with open(settings.INTERACTION_MAP_PATH, 'wb') as f:
        pickle.dump({
            'pairs': pairs,
            'severities': severities,
            'descriptions': descriptions,
            'risk_levels': risk_levels,
            'affected_organs': affected_organs,
            'pair_map': pair_map
        }, f)

    print("Model training complete. Assets saved to:", settings.MODEL_ASSETS_DIR)

if __name__ == "__main__":
    main()