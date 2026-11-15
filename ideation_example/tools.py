from bottle import request, response as bottle_response, route, run
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@route('/get_idea', method='GET')
def get_idea():
    bottle_response.content_type = "application/json"
    
    return json.dumps({
        "status": "success",
        "idea_description": {
            "acronym": "SmartShelf",
            "idea_type": "product",
            "idea_impact": "High efficiency gain in retail",
            "brand": "thorn",
            "applications": "Retail, Art & Culture",
            "description": "An AI-powered modular shelf system that tracks inventory in real-time and dynamically adjusts digital price tags.",
            "reason": "Reduce out-of-stock situations and manual labor",
            "audience": "Store managers and museum curators",
            "status": "submitted"
        }
    })


@route('/competitive_landscape', method='POST')
def competitive_landscape():
    bottle_response.content_type = "application/json"

    input_data = request.json or {}
    idea = input_data.get("idea_description", {})

    acronym = idea.get("acronym", "None")
    idea_type = idea.get("idea_type", "None")
    idea_impact = idea.get("idea_impact", "None")
    brand = idea.get("brand", "None")
    applications = idea.get("applications", "None")
    description = idea.get("description", "None")
    reason = idea.get("reason", "None")
    audience = idea.get("audience", "Allgemein")
    status = idea.get("status", "None")

    prompt = f"""
    You are an expert market research and competitive intelligence agent.
    Evaluate the following product idea regarding its competitive landscape and market positioning:

    Product Acronym: {acronym}
    Idea Type: {idea_type}
    Idea Impact: {idea_impact}
    Brand: {brand}
    Target Applications: {applications}
    Target Audience: {audience}
    Description: {description}
    Reason: {reason}
    Status: {status}

    Your tasks:
    1. Identify potential main competitors (1-5) or competitive alternatives.
    2. Evaluate the product across 6 core metrics on a scale from 1 to 10 (1 = low, 10 = high):
       - range breadth
       - aesthetics
       - market price
       - efficiency
       - lifetime
       - controlability
    3. Evaluate the competitors based on the same metrics and create the spider graph structure.

    Please return your output ONLY as a valid JSON object matching this exact structure:
    {{
      "competitive_landscape": "Short textual summary of the competitive landscape.",
      "spider": [
        ["category", "brand", "competitor 1", "competitor 2"],
        ["range breadth", 8, 5, 7],
        ["aesthetics", 7, 6, 8],
        ["market price", 6, 7, 5],
        ["efficiency", 9, 6, 7],
        ["lifetime", 8, 7, 6],
        ["controlability", 8, 6, 7]
      ]
    }}
    """

    try:
        openai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        agent_message = openai_response.choices[0].message.content
        parsed_data = json.loads(agent_message)

    except Exception as e:
        parsed_data = {
            "competitive_landscape": "",
            "spider": []
        }

    ret = {
        "status": "success",
        "competitive_landscape": parsed_data.get("competitive_landscape", ""),
        "spider": parsed_data.get("spider", [])
    }
    
    return json.dumps(ret)


@route('/application_trends', method='POST')
def application_trends():
    bottle_response.content_type = "application/json"

    input_data = request.json or {}
    idea = input_data.get("idea_description", {})

    acronym = idea.get("acronym", "None")
    idea_type = idea.get("idea_type", "None")
    idea_impact = idea.get("idea_impact", "None")
    brand = idea.get("brand", "None")
    applications = idea.get("applications", "None")
    description = idea.get("description", "None")
    reason = idea.get("reason", "None")
    audience = idea.get("audience", "Allgemein")
    status = idea.get("status", "None")

    prompt = f"""
    You are an expert technology and industry trends analyst agent.
    Evaluate current application trends, market adoption drivers, and future relevance for the following product idea:

    Product Acronym: {acronym}
    Idea Type: {idea_type}
    Idea Impact: {idea_impact}
    Brand: {brand}
    Target Applications: {applications}
    Target Audience: {audience}
    Description: {description}
    Reason: {reason}
    Status: {status}

    Your tasks:
    1. Analyze current digital and market trends relevant to the specified target applications (e.g., Retail, Art & Culture).
    2. Evaluate how well the product aligns with these emerging application trends.

    Please return your output ONLY as a valid JSON object matching this exact structure:
    {{
      "summary": "Concise summary of trends and application fit in maximum 5 sentences."
    }}
    """

    try:
        openai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        agent_message = openai_response.choices[0].message.content
        parsed_data = json.loads(agent_message)
        summary_text = parsed_data.get("summary", "")

    except Exception as e:
        summary_text = ""

    ret = {
        "status": "success",
        "application_trends": summary_text
    }
    
    return json.dumps(ret)


@route('/competitive_benchmarking', method='POST')
def competitive_benchmarking():
    bottle_response.content_type = "application/json"

    input_data = request.json or {}
    idea = input_data.get("idea_description", {})

    acronym = idea.get("acronym", "None")
    idea_type = idea.get("idea_type", "None")
    idea_impact = idea.get("idea_impact", "None")
    brand = idea.get("brand", "None")
    applications = idea.get("applications", "None")
    description = idea.get("description", "None")
    reason = idea.get("reason", "None")
    audience = idea.get("audience", "Allgemein")
    status = idea.get("status", "None")

    prompt = f"""
    You are a competitive benchmarking specialist.
    Benchmark the following product idea against key market alternatives, focusing on USPs, technological advantages, and market barriers:

    Product Acronym: {acronym}
    Idea Type: {idea_type}
    Idea Impact: {idea_impact}
    Brand: {brand}
    Target Applications: {applications}
    Target Audience: {audience}
    Description: {description}
    Reason: {reason}
    Status: {status}

    Please return your output ONLY as a valid JSON object matching this exact structure:
    {{
      "benchmarking": "Concise summary of competitive benchmarking in maximum 5 sentences."
    }}
    """

    try:
        openai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        agent_message = openai_response.choices[0].message.content
        parsed_data = json.loads(agent_message)
        benchmarking_text = parsed_data.get("benchmarking", "")

    except Exception as e:
        benchmarking_text = ""

    ret = {
        "status": "success",
        "competitive_benchmarking": benchmarking_text
    }
    
    return json.dumps(ret)


@route('/financial_data', method='POST')
def financial_data():
    bottle_response.content_type = "application/json"

    input_data = request.json or {}
    idea = input_data.get("idea_description", {})

    acronym = idea.get("acronym", "None")
    idea_type = idea.get("idea_type", "None")
    idea_impact = idea.get("idea_impact", "None")
    brand = idea.get("brand", "None")
    applications = idea.get("applications", "None")
    description = idea.get("description", "None")
    reason = idea.get("reason", "None")
    audience = idea.get("audience", "Allgemein")
    status = idea.get("status", "None")

    prompt = f"""
    You are a corporate financial analyst and portfolio strategist.
    Estimate realistic financial metrics and portfolio fit parameters for the following product idea:

    Product Acronym: {acronym}
    Idea Type: {idea_type}
    Idea Impact: {idea_impact}
    Brand: {brand}
    Target Applications: {applications}
    Target Audience: {audience}
    Description: {description}
    Reason: {reason}
    Status: {status}

    Return your output ONLY as a valid JSON object matching this exact structure:
    {{
      "portfolio_review": [
        {{"metric": "Estimated R&D Cost", "value": "€150,000", "assessment": "Medium"}},
        {{"metric": "Target Gross Margin", "value": "45%", "assessment": "High"}},
        {{"metric": "Expected Payback Period", "value": "2.5 Years", "assessment": "Favorable"}},
        {{"metric": "Portfolio Fit Index", "value": "8.5 / 10", "assessment": "Strategic High"}}
      ]
    }}
    """

    try:
        openai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        agent_message = openai_response.choices[0].message.content
        parsed_data = json.loads(agent_message)

    except Exception as e:
        parsed_data = {"portfolio_review": []}

    ret = {
        "status": "success",
        "portfolio_review": parsed_data.get("portfolio_review", [])
    }
    
    return json.dumps(ret)


# simulate user task
@route('/stakeholders', method='POST')
def stakeholders():
    bottle_response.content_type = "application/json"

    input_data = request.json or {}
    idea = input_data.get("idea_description", {})
    applications = idea.get("applications", "").lower()

    # Statische / Simulierte Logik je nach Anwendungsbereich
    if "retail" in applications:
        buyer = "Store Manager"
        stakeholders_list = ["Store Manager", "Inventory Clerk", "Store Owner"]
        stakes = [
            ["Store Manager", "high"],
            ["Inventory Clerk", "middle"],
            ["Store Owner", "high"]
        ]
    elif "art" in applications or "culture" in applications:
        buyer = "Museum Curator"
        stakeholders_list = ["Museum Curator", "Exhibition Designer", "Visitor Services Lead"]
        stakes = [
            ["Museum Curator", "high"],
            ["Exhibition Designer", "middle"],
            ["Visitor Services Lead", "low"]
        ]
    else:
        buyer = "Operations Manager"
        stakeholders_list = ["Operations Manager", "Department Lead", "End User"]
        stakes = [
            ["Operations Manager", "high"],
            ["Department Lead", "middle"],
            ["End User", "low"]
        ]

    return json.dumps({
        "status": "success",
        "buyer": buyer,
        "stakeholders": stakeholders_list,
        "stakes": stakes
    })


# simulate user task
@route('/jobs_done', method='POST')
def jobs_done():
    bottle_response.content_type = "application/json"

    input_data = request.json or {}
    stakeholders_list = input_data.get("stakeholders", ["Store Manager"])

    jobs_analysis = []
    for sh in stakeholders_list:
        if "Manager" in sh or "Curator" in sh:
            jobs_analysis.append({
                "stakeholder": sh,
                "job": "Monitor daily performance and resource availability efficiently.",
                "struggle": "Manual data tracking is time-consuming and prone to human error."
            })
        elif "Clerk" in sh or "Designer" in sh:
            jobs_analysis.append({
                "stakeholder": sh,
                "job": "Execute operational setup and maintain day-to-day layouts.",
                "struggle": "Lack of real-time visibility leads to delays and stock mismatches."
            })
        else:
            jobs_analysis.append({
                "stakeholder": sh,
                "job": "Ensure smooth workflow integration and quality standards.",
                "struggle": "Complex setup processes and insufficient training materials."
            })

    return json.dumps({
        "status": "success",
        "jobs_analysis": jobs_analysis
    })


@route('/final_judgment', method='POST')
def final_judgment():
    bottle_response.content_type = "application/json"

    input_data = request.json or {}
    
    spider = input_data.get("spider", [])
    landscape = input_data.get("competitive_landscape", "")
    trends = input_data.get("application_trends", "")
    benchmarking = input_data.get("competitive_benchmarking", "")
    portfolio = input_data.get("portfolio_review", [])
    stakes = input_data.get("stakes", [])
    jobs = input_data.get("all_apps", [])

    prompt = f"""
    You are the Chief Innovation Officer and Executive Decision Agent.
    Review all collected analysis data for a product idea and make a final recommendation whether to PROCEED with development or WITHDRAW the project.

    Collected Input Data:
    - Competitive Landscape Summary: {landscape}
    - Spider Graph Scores: {spider}
    - Application Trends: {trends}
    - Competitive Benchmarking: {benchmarking}
    - Portfolio & Financial Review: {portfolio}
    - Stakeholder Mapping: {stakes}
    - Jobs-to-be-Done Analysis: {jobs}

    Tasks:
    1. Synthesize all key findings (strengths vs. risks).
    2. Make a clear decision: "proceed" or "withdraw".
    3. Provide a concise, bulleted executive justification (max 3-4 key reasons).

    Return your output ONLY as a valid JSON object matching this exact structure:
    {{
      "decision": "proceed",  
      "justification": "Short executive rationale explaining why to proceed or withdraw.",
      "key_drivers": ["Reason 1", "Reason 2", "Reason 3"]
    }}
    """

    try:
        openai_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        agent_message = openai_response.choices[0].message.content
        parsed_data = json.loads(agent_message)
    except Exception as e:
        parsed_data = {
            "decision": "withdraw",
            "justification": "",
            "key_drivers": []
        }

    ret = {
        "status": "success",
        "decision": parsed_data.get("decision", "withdraw"),
        "justification": parsed_data.get("justification", ""),
        "key_drivers": parsed_data.get("key_drivers", [])
    }
    
    return json.dumps(ret)


if __name__ == "__main__":
    run(host="localhost", port=4569, debug=True)