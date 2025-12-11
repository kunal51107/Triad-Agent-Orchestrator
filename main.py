import os
import re
from dotenv import load_dotenv
from agents import SearcherAgent, AnalystAgent, StructurerAgent
from colorama import Fore, Style, init

# 1. Initialize environment and colors
load_dotenv()
init(autoreset=True)

def sanitize_filename(query):
    """
    Cleans the query to make a safe filename.
    Removes special characters and limits length.
    """
    # Keep only alphanumeric and spaces, then replace spaces with underscores
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', query)
    return clean.replace(' ', '_')[:50]

def main():
    print(Fore.CYAN + Style.BRIGHT + "\n========================================")
    print(Fore.CYAN + Style.BRIGHT + "   TRIAD AGENT ORCHESTRATOR   ")
    print(Fore.CYAN + Style.BRIGHT + "========================================")
    print(Fore.WHITE + "Pipeline: Tavily (Search) -> Gemini (Analyze) -> Groq (Structure)\n")

    while True:
        # --- INPUT PHASE ---
        user_query = input(Fore.YELLOW + "Enter your research topic (or 'q' to quit): " + Fore.RESET)
        
        if user_query.lower() in ['q', 'quit', 'exit']:
            print(Fore.CYAN + "\nShutting down. Goodbye!")
            break
        
        if not user_query.strip():
            continue

        print(Fore.WHITE + "-" * 60)
        start_time = time.time()

        try:
            # --- INITIALIZE AGENTS ---
            # We re-init agents per loop to ensure clean state
            searcher = SearcherAgent()
            analyst = AnalystAgent()
            structurer = StructurerAgent()

            # --- STEP 1: SEARCHER ---
            print(Fore.GREEN + "1. [Searcher AI] " + Fore.WHITE + f"Scanning web for: '{user_query}'...")
            raw_data = searcher.search(user_query)
            
            # Check for immediate search failure
            if "error" in raw_data.lower() and "search failed" in raw_data.lower():
                print(Fore.RED + "Search failed. Please check your internet or API key.")
                continue

            # --- STEP 2: ANALYST ---
            print(Fore.GREEN + "2. [Analyst AI]  " + Fore.WHITE + "Synthesizing data & checking logic (Gemini)...")
            analysis_json = analyst.analyze(raw_data)

            # --- STEP 3: STRUCTURER ---
            print(Fore.GREEN + "3. [Structurer AI]" + Fore.WHITE + "Formatting final report (Llama 3)...")
            final_report = structurer.structure(analysis_json)

            # --- OUTPUT PHASE ---
            print(Fore.CYAN + "\n" + "="*20 + " FINAL REPORT " + "="*20 + "\n")
            print(final_report)
            print(Fore.CYAN + "\n" + "="*54)

            # --- SAVE TO FILE ---
            filename = f"Report_{sanitize_filename(user_query)}.md"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(final_report)
            
            elapsed = round(time.time() - start_time, 2)
            print(Fore.MAGENTA + f"\n Report saved to: {filename}")
            print(Fore.MAGENTA + f" Total time elapsed: {elapsed} seconds\n")

        except Exception as e:
            print(Fore.RED + f"\n Pipeline Error: {e}")
            print(Fore.WHITE + "Tip: Check your API keys in .env or your internet connection.\n")

import time # Imported late for the timer logic

if __name__ == "__main__":
    main()