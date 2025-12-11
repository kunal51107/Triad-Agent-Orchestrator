import os
import json
import time
from typing import Dict, Any
from tavily import TavilyClient
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq

# Load environment variables once at module level
load_dotenv()

class SearcherAgent:
    """
    Agent responsible for retrieving factual information from the web 
    using the Tavily API.
    """
    
    def __init__(self):
        self.role = "Searcher AI"
        api_key = os.getenv("TAVILY_API_KEY")
        
        if not api_key:
            raise ValueError("ERROR: 'TAVILY_API_KEY' is missing from .env file.")
        
        self.client = TavilyClient(api_key=api_key)

    def search(self, query: str) -> str:
        """
        Executes a web search and returns the results as a JSON-formatted string.
        """
        print(f"[{self.role}] Running query: '{query}'")
        
        try:
            # 'search_depth="basic"' is faster and cheaper. 
            # Use "advanced" if you need deep research later.
            response = self.client.search(
                query=query, 
                search_depth="basic", 
                max_results=3,
                include_answer=True # Tavily generates a short direct answer too
            )
            
            # Construct a clean dictionary to return
            clean_results = {
                "query_used": query,
                "tavily_answer": response.get('answer', ''), # The direct answer
                "sources": []
            }

            # Loop through results and pick only what we need
            for res in response.get('results', []):
                clean_results["sources"].append({
                    "title": res.get('title'),
                    "url": res.get('url'),
                    "content": res.get('content')
                })

            # Return as JSON string for the next agent to read
            return json.dumps(clean_results, indent=2)

        except Exception as e:
            # Return the error in JSON so the pipeline doesn't crash
            error_msg = {"error": f"Search failed: {str(e)}"}
            return json.dumps(error_msg, indent=2)

class AnalystAgent:
    """
    Agent responsible for synthesizing search data using Google Gemini.
    """
    def __init__(self):
        self.role = "Analyst AI"
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("ERROR: 'GEMINI_API_KEY' is missing.")
        
        # Configure Gemini
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-flash-latest')

    def analyze(self, search_data: str) -> str:
        print(f"[{self.role}] Analyzing data...")
        
        # The prompt forces Gemini to act as a logic layer
        prompt = f"""
        You are an Expert Knowledge Analyst.
        
        Input Data:
        {search_data}
        
        Your Mission:
        1. **Analyze the Intent**: Is this a technical query, a news update, a historical question, or a product comparison?
        2. **Synthesize**: Merge the search results into a cohesive narrative.
        3. **Enrich**: Use your internal knowledge to explain *why* this matters, defining technical terms or adding historical context where missing.
        4. **Verify**: if sources conflict, note it.
        
        Output strictly valid JSON with these dynamic fields:
        {{
            "topic_type": "e.g., Technical Comparison / Breaking News / Biography",
            "core_answer": "The main, direct answer to the user's query.",
            "detailed_analysis": "A deep dive into the nuances, facts, and figures found.",
            "expert_context": "Your added internal knowledge that gives the user the 'big picture'."
        }}
        """

        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(prompt)
                clean_text = response.text.replace("```json", "").replace("```", "").strip()
                return clean_text
            
            except Exception as e:
                if "429" in str(e):
                    wait_time = (attempt + 1) * 10  # Wait 10s, then 20s, etc.
                    print(f"[{self.role}] Rate Limit Hit. Waiting {wait_time}s before retry...")
                    time.sleep(wait_time)
                else:
                    return json.dumps({"error": f"Analysis failed: {str(e)}"})
        
        return json.dumps({"error": "Failed after max retries."})

class StructurerAgent:
    def __init__(self):
        self.role = "Structurer AI"
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("ERROR: 'GROQ_API_KEY' is missing.")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile" 

    def structure(self, analysis_data: str) -> str:
        print(f"[{self.role}] Adapting layout to content type...")
        
        prompt = f"""
        You are an elite Editor and Content Strategist.
        
        Input Analysis:
        {analysis_data}
        
        Your Goal:
        Transform the input JSON into the **most effective Markdown format possible** for this specific topic.
        
        **Dynamic Formatting Rules:**
        1. **Identify the Vibe**: 
           - If it's a **Comparison** (e.g., "X vs Y"), use specific comparison tables.
           - If it's **Code/Technical**, use code blocks and step-by-step implementation guides.
           - If it's **News**, use a "Key Takeaways" style with chronological updates.
           - If it's **History/Biography**, use a narrative flow or timeline.
        
        2. **No Rigid Templates**: Do NOT force sections like "Gap Analysis" or "Executive Summary" unless they actually fit the content. 
        
        3. **Style**: 
           - Use professional Markdown (H1, H2, Bold, Tables, Blockquotes).
           - Make it readable, engaging, and authoritative.
           - Start with a strong, relevant title.
        
        Return ONLY the Markdown text.
        """
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a chameleon editor who adapts format to content."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.6, 
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Error structuring report: {str(e)}"
        
# TEST (FULL CHAIN) ---
if __name__ == "__main__":
    searcher = SearcherAgent()
    raw_json = searcher.search("Compare iPhone 16 Pro vs Samsung S25 Ultra specs")
    
    analyst = AnalystAgent()
    analysis_result = analyst.analyze(raw_json)
    
    structurer = StructurerAgent()
    final_report = structurer.structure(analysis_result)
    
    print("\n=== FINAL REPORT ===\n")
    print(final_report)