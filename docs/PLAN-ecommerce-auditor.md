# PLAN-ecommerce-auditor

## 1. Goal
Build "The E-commerce AI Opportunity Auditor," a Streamlit web application that scrapes e-commerce sites (focusing on JSON-LD/Metadata) and uses GPT-4o to generate 3 high-impact AI automation opportunities. The tool must feel like a premium "Consultant Report" and handle anti-bot measures gracefully.

## 2. Architecture & Tech Stack
*   **Language**: Python 3.10+
*   **UI Framework**: Streamlit
*   **Scraping**: `requests`, `BeautifulSoup4`
*   **AI**: OpenAI API (GPT-4o)
*   **Styling**: Custom CSS (Tailwind-like, Dark Mode)

## 3. Core Features
1.  **Input Layer**:
    *   Sidebar inputs for URL and OpenAI API Key.
    *   Validation for URL format.
2.  **Smart Scraping Engine**:
    *   **Strategy**: "Lightweight Reliability".
    *   **Logic**:
        1.  Rotate User-Agents (Chrome, Firefox, Safari).
        2.  Fetch HTML.
        3.  **Primary**: Extract `<script type="application/ld+json">` (Product/Organization schema).
        4.  **Secondary**: Extract Meta Title, Description, H1, H2s.
    *   **Error Handling**: If 403 Forbidden -> Display "Security Shield Detected" badge (Selling point).
3.  **AI Consultant Brain**:
    *   System Prompt: Senior AI Consultant.
    *   Input: Scraped JSON-LD + Metadata.
    *   Output: 3 distinct opportunities (e.g., Returns Agent, Product Matcher MCP).
    *   Metrics: "Project Complexity" (Low/Med/High), "Potential ROI" (1-10 Scale).
4.  **Presentation Layer**:
    *   "Premium Consultant" Theme (Dark background, clear typography, cards).
    *   Display structured opportunities in `st.columns`.
    *   Footer: "Built by Hugo Platret | Senior AI Consultant in Utrecht".
5.  **Deliverable Generation**:
    *   "Download Report" button.
    *   Generates a structured Markdown/Text file with the analysis.

## 4. Implementation Steps

### Phase 1: Setup & Scraping Core
- [ ] Initialize project structure and `requirements.txt`.
- [ ] Implement `fetch_page_content(url)` with User-Agent rotation.
- [ ] Implement `extract_structured_data(html)`:
    - [ ] JSON-LD parser.
    - [ ] Fallback metadata parser.
- [ ] Handle 403/Connection errors with "Consultant Messaging".

### Phase 2: AI Logic & Integration
- [ ] Create `analyze_commerce_data(data, api_key)` function.
- [ ] Design Prompt for GPT-4o to output structured JSON/Strict format.
- [ ] Test with sample e-commerce sites (Shopify, WooCommerce, Custom).

### Phase 3: UI & Experience (Streamlit)
- [ ] Apply Custom CSS (Dark Mode, Cards).
- [ ] Build Sidebar (Inputs).
- [ ] Build Main Feed:
    - [ ] Loading states ("Auditing Store...", "Analyzing Opportunities...").
    - [ ] Success state (The Report).
    - [ ] "Security Shield" State.
- [ ] Implement "Download Report" functionality.

### Phase 4: Verification & Polish
- [ ] Verify JSON-LD extraction on major platforms.
- [ ] Verify "Download" works locally and in cloud environment.
- [ ] Final UI Polish (Footer, fonts, spacing).

## 5. Verification Checklist
- [ ] **Scraping**: Can successfully extract JSON-LD from a standard Shopify product page?
- [ ] **Resilience**: Does a 403 error show the "Security Shield" message instead of crashing?
- [ ] **AI**: Does GPT-4o return exactly 3 opportunities?
- [ ] **UX**: Is the design "Premium Dark Mode"?
- [ ] **Output**: Does the downloaded file match the on-screen content?
