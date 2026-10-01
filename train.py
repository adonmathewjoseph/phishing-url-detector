import math
import re
from urllib.parse import urlparse
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def extract_features(url: str) -> dict:
    clean_url = url if url.startswith(("http://", "https://")) else "http://" + url
    parsed = urlparse(clean_url)
    hostname = parsed.hostname or ""
    path = parsed.path or ""

    # Check for raw IP address
    ip_pattern = r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$"
    has_ip = 1 if re.match(ip_pattern, hostname) else 0

    # Shannon entropy of characters
    prob = [float(url.count(c)) / len(url) for c in dict.fromkeys(list(url))]
    entropy = -sum([p * math.log(p) / math.log(2.0) for p in prob]) if url else 0

    return {
        "url_length": len(url),
        "hostname_length": len(hostname),
        "path_length": len(path),
        "count_dots": url.count("."),
        "count_hyphens": url.count("-"),
        "count_at": url.count("@"),
        "count_slash": url.count("/"),
        "count_question": url.count("?"),
        "count_equal": url.count("="),
        "has_ip": has_ip,
        "subdomain_count": max(0, len(hostname.split(".")) - 2),
        "entropy": round(entropy, 4),
        "is_https": 1 if url.startswith("https://") else 0,
    }

def main():
    print("1. Loading dataset.csv...")
    df = pd.read_csv("dataset.csv").dropna().drop_duplicates()

    print("2. Extracting lexical features...")
    feature_list = [extract_features(u) for u in df["URL"]]
    X = pd.DataFrame(feature_list)
    y = df["Label"].apply(lambda x: 1 if x == "bad" else 0)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print("3. Training Random Forest model on M1 CPU...")
    model = RandomForestClassifier(n_estimators=100, max_depth=12, n_jobs=-1, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    print("\nModel Performance:")
    print(classification_report(y_test, predictions, target_names=["Safe", "Phishing"]))

    joblib.dump(model, "phishing_model.pkl")
    print("4. Done! Model saved as 'phishing_model.pkl'.")

if __name__ == "__main__":
    main()
