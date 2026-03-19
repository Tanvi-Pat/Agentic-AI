from graph import build_graph
import sys
from dotenv import load_dotenv
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
load_dotenv(override=True)

app = build_graph()
print(sys.argv[1])
result = app.invoke({"domain": sys.argv[1], "candidates": [],
                     "financial_scores": {}, "risk_scores": {},
                     "ai_scores": {},"financial_raw": {}, "risk_raw": {},
                     "ai_raw": {}, "ranked_list": [], "final_report": ""})

                     