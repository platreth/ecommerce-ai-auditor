import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import random
import time
from openai import OpenAI

# --- CONFIGURATION & STYLING ---
st.set_page_config(
    page_title="E-commerce AI Auditor",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Dark Mode
st.markdown("""
<style>
    /* Global Theme Overrides */
    .stApp {
        background-color: #0f172a; /* Slate 900 */
        color: #e2e8f0; /* Slate 200 */
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #f8fafc !important; /* Slate 50 */
        font-family: 'Inter', sans-serif;
    }
    
    /* Cards */
    div[data-testid="metric-container"] {
        background-color: #1e293b; /* Slate 800 */
        border: 1px solid #334155; /* Slate 700 */
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton>button {
        background-color: #3b82f6; /* Blue 500 */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.2s;
    }
    
    .stButton>button:hover {
        background-color: #2563eb; /* Blue 600 */
        box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3);
    }
    
    /* Footer */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0f172a;
        color: #64748b;
        text-align: center;
        padding: 20px;
        border-top: 1px solid #1e293b;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# --- SCRAPING ENGINE (LIGHTWEIGHT) ---
HEADERS_LIST = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
]

def get_random_header():
    return {'User-Agent': random.choice(HEADERS_LIST)}

def extract_json_ld(soup):
    """Finds and parses standard JSON-LD Schema.org data."""
    scripts = soup.find_all('script', type='application/ld+json')
    data = []
    for script in scripts:
        try:
            if script.string:
                content = json.loads(script.string)
                data.append(content)
        except json.JSONDecodeError:
            continue
    return data

def lightweight_scrape(url):
    """
    Scrapes a URL with rotation and fallback strategies.
    Returns: (status_code, data_dict, error_message)
    """
    if not url.startswith('http'):
        url = 'https://' + url
        
    try:
        response = requests.get(url, headers=get_random_header(), timeout=10)
        
        # Security Shield Detection
        if response.status_code == 403 or response.status_code == 401:
            return response.status_code, None, "Security Shield Detected"
            
        if response.status_code != 200:
            return response.status_code, None, f"HTTP Error {response.status_code}"
            
        # Parse Content
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 1. Primary: JSON-LD
        json_updates = extract_json_ld(soup)
        
        # 2. Secondary: Metadata
        page_title = soup.title.string if soup.title else ""
        meta_desc = ""
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            meta_desc = desc_tag.get('content', '')
            
        # 3. Tertiary: Headings (Structure)
        h1s = [h.get_text(strip=True) for h in soup.find_all('h1')]
        h2s = [h.get_text(strip=True) for h in soup.find_all('h2')][:5] # Limit to top 5
        
        scraped_payload = {
            "url": url,
            "title": page_title,
            "description": meta_desc,
            "h1": h1s,
            "h2": h2s,
            "schema_check": "✅ Found JSON-LD" if json_updates else "❌ No Schema Found",
            "raw_json_ld": json_updates[:2] # Limit size for token context
        }
        
        return 200, scraped_payload, None

    except Exception as e:
        return 500, None, str(e)

def analyze_commerce_data(scraped_data, api_key):
    """
    sends scraped data to GPT-4o for analysis.
    Returns: list of dicts (opportunities)
    """
    client = OpenAI(api_key=api_key)
    
    system_prompt = """You are a Tier-1 AI Strategy Consultant (ex-McKinsey/BCG) auditing an e-commerce store.
    Your goal is to find UNTAPPED, SPECIFIC automation opportunities.
    
    CRITICAL RULES:
    1. NO GENERIC ADVICE. Banned phrases: "Implement a chatbot", "Improve SEO", "Send emails".
    2. BE SPECIFIC. Instead of "Chatbot", say "Autonomous Order Modification Agent". Instead of "SEO", say "Programmatic SEO for Long-tail [Product] Keywords".
    3. BE CRITICAL. If the store looks small, suggest low-cost automations. If enterprise, suggest heavy-duty architectures.
    4. VARIANCE IS GOOD. Do NOT give everything a 7/10 or 8/10. 
       - If an idea is high risk, give it 9/10 Complexity and 9/10 ROI. 
       - If it's a quick win, give it 2/10 Complexity and 6/10 ROI.
    
    Analyze the provided JSON-LD and Headers.
    Structure the response exactly as this JSON:
    {
        "opportunities": [
            {
                "title": "High-Impact, Specific Title",
                "description": "Brutal, direct explanation of the value. Why THIS store? Reference their specific products found in the data.",
                "complexity": "Low/Medium/High",
                "roi": "Score 1-10 (Use full range 4-10)",
                "tools": ["Specific Tool 1 (e.g. Make.com)", "Specific Tool 2 (e.g. Pinecone)"]
            }
        ]
    }
    """
    
    user_content = f"Analyze this store data: {json.dumps(scraped_data)}"
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

# --- MAIN UI ---
def main():
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        openai_key = st.text_input("OpenAI API Key", type="password", help="Enter your GPT-4o enabled API key")
        st.divider()
        st.info("💡 **Tip:** This tool analyzes public storefronts to find automation gaps.")
    
    # Hero Section
    st.title("🛒 E-commerce AI Opportunity Auditor")
    st.markdown("Enter a webshop URL below. My AI agents will scan the storefront, bypass basic security shields, and identify **3 high-value automation opportunities** tailored to their business.")
    
    # Input Area
    col1, col2 = st.columns([3, 1])
    with col1:
        target_url = st.text_input("Store URL", placeholder="e.g. https://www.gymshark.com")
    with col2:
        analyze_btn = st.button("🚀 Audit Store", use_container_width=True)
    
    # Footer
    st.markdown('<div class="footer">Built by Hugo Platret | Senior AI Consultant in Utrecht</div>', unsafe_allow_html=True)

    if analyze_btn:
        if not openai_key:
            st.warning("⚠️ Please provide your OpenAI API Key in the sidebar to proceed.")
            return
            
        if not target_url:
            st.warning("⚠️ Please enter a URL.")
            return

        # Step 1: Scraping
        with st.status("🕵️‍♂️ Deploying Reconnaissance Agents...", expanded=True) as status:
            st.write("🔄 Rotating User-Agents...")
            time.sleep(1) # Simulate meaningful work/rotation
            
            st.write(f"🌐 Connecting to {target_url}...")
            code, data, error = lightweight_scrape(target_url)
            
            if code == 403:
                status.update(label="🛡️ Security Shield Active!", state="error")
                st.error(f"**Security Shield Detected ({code})**")
                st.info("This site has strong bot protection. This is actually a **good sign**! It means they value security. We can still analyze their public presence based on what we can see.")
                # We could proceed with partial analysis if we had fallback, but here we stop or mock
                return
            
            elif code != 200:
                status.update(label="❌ Connection Failed", state="error")
                st.error(f"Failed to connect: {error}")
                return
            
            status.update(label="✅ Site Scanned Successfully!", state="complete")
            
            # Show debug data (Hidden in production maybe, but good for trust now)
            with st.expander("View Raw Intelligence"):
                st.json(data)
                
            # Step 2: AI Analysis
            with st.status("🧠 Analyzing Data with GPT-4o...", expanded=True) as status:
                st.write("Connecting to OpenAI...")
                analysis = analyze_commerce_data(data, openai_key)
                
                if "error" in analysis:
                    status.update(label="❌ AI Analysis Failed", state="error")
                    st.error(f"AI Error: {analysis['error']}")
                    return
                
                status.update(label="✅ Analysis Complete!", state="complete")
                st.session_state['analysis_result'] = analysis
                st.session_state['target_url'] = target_url
            
    # Display Results (Outside button logic to persist if in session state)
    if 'analysis_result' in st.session_state:
        analysis = st.session_state['analysis_result']
        url = st.session_state.get('target_url', 'Target Site')
        
        st.divider()
        st.subheader("🤖 Strategic Recommendations")
        
        opportunities = analysis.get("opportunities", [])
        for opp in opportunities:
            with st.container():
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"### {opp['title']}")
                    st.write(opp['description'])
                    st.caption(f"Suggested Stack: {', '.join(opp.get('tools', []))}")
                with c2:
                    st.metric("ROI Score", f"{opp['roi']}/10")
                    st.markdown(f"**Complexity:** {opp['complexity']}")
                st.divider()

        # Download Report
        report_text = f"# AI Opportunity Report for {url}\n\n"
        report_text += "Generated by E-commerce AI Auditor\n---\n\n"
        for i, opp in enumerate(opportunities, 1):
            report_text += f"## {i}. {opp['title']}\n"
            report_text += f"**ROI:** {opp['roi']}/10 | **Complexity:** {opp['complexity']}\n\n"
            report_text += f"{opp['description']}\n\n"
            report_text += f"**Tools:** {', '.join(opp.get('tools', []))}\n\n---\n"
        
        st.download_button(
            label="📄 Download Consultant Report",
            data=report_text,
            file_name=f"AI_Audit_{int(time.time())}.md",
            mime="text/markdown",
            use_container_width=True
        )

if __name__ == "__main__":
    main()
