Agentic Orchestration for Product Research

It produces a detailed product report entailing an market anlysis of top product models/brands based on the product and the product requirements mentioned in the input. This report consists of comparison of various brands/models by listing their pros and cons.

The agent named product_manager contains three agent turned tools and one handoff.
1. Plan searches: This tool creates different search queries based on the input query to be passed on to Web search tool.
2. Web Search: This tool extracts important product information needed to create a detailed product report. 
3. Report writer: This tool writes a detailed report based on the available information.
4. Email agent: This handoff takes in the report and shoots an email with the report to the email of interest. 