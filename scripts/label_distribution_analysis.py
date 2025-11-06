import json
import os
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd

def analyze_label_distribution(doc_ids, json_dir='data/raw/funsd/dataset/training_data/annotations'):
    """Reads multiple JSON files and counts the high-level labels."""
    label_counts = defaultdict(int)
    total_tokens = 0
    
    for doc_id in doc_ids:
        json_path = os.path.join(json_dir, f'{doc_id}.json')
        
        try:
            # --- FIX APPLIED HERE: Added encoding='utf-8' ---
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"Skipping {doc_id}: JSON file not found.")
            continue
        # Catch the decode error, though the fix should prevent it
        except UnicodeDecodeError:
            print(f"Skipping {doc_id}: Encoding error encountered.")
            continue
            
        # The FUNSD JSON is structured by entities in the 'form' list.
        for entity in data['form']:
            label = entity.get('label', 'other') 
            
            # Count the total number of words (tokens) within each entity.
            words_in_entity = entity.get('words', [])
            num_tokens = len(words_in_entity)
            
            # Map FUNSD labels to our analysis groups
            if label in ['question', 'answer']:
                label_counts['Meaningful_Entity'] += num_tokens
            elif label in ['header', 'other']:
                label_counts['Irrelevant_Context'] += num_tokens
            else:
                label_counts['Irrelevant_Context'] += num_tokens
                
            total_tokens += num_tokens
            
    label_counts['Total_Tokens'] = total_tokens
    return label_counts

# Sample 10 document IDs (Use IDs available in your FUNSD data)
sample_doc_ids = ['00040534', '00070353', '00093726', '00283813', '660978'] # Replace with your actual IDs

counts = analyze_label_distribution(sample_doc_ids)

print("\n--- Label Distribution Counts ---")
print(f"Total Tokens Analyzed: {counts['Total_Tokens']}")
meaningful_count = counts['Meaningful_Entity']
irrelevant_count = counts['Irrelevant_Context']
print(f"Meaningful Entities (Question/Answer): {meaningful_count}")
print(f"Irrelevant Context (O-Tag): {irrelevant_count}")

# Calculate Imbalance Percentage
imbalance_ratio = (irrelevant_count / counts['Total_Tokens']) * 100
print(f"\nEstimated 'O' Token Percentage: {imbalance_ratio:.2f}%")


# Data for the chart
data = {
    'Category': ['Meaningful Entities (Q/A)', 'Irrelevant Context (O-Tag)'],
    'Token Count': [meaningful_count, irrelevant_count]
}
df = pd.DataFrame(data)

# Create the Bar Chart
plt.figure(figsize=(8, 6))
bars = plt.bar(df['Category'], df['Token Count'], color=['#4CAF50', '#FF5733'])
plt.title('Token Distribution: Justification for Class Imbalance Handling')
plt.ylabel('Total Number of Tokens')
plt.xlabel('Token Category')
plt.xticks(rotation=0)

# Add percentage labels on top of the bars
for bar in bars:
    height = bar.get_height()
    percentage = (height / counts['Total_Tokens']) * 100
    plt.text(bar.get_x() + bar.get_width() / 2., 
             height + 50, 
             f'{percentage:.1f}%',
             ha='center', 
             va='bottom', 
             fontsize=10)

plt.tight_layout()
plt.savefig('eda_label_distribution.png')
plt.show()