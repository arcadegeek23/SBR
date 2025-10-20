"""
Azure AI Foundry Service
Handles integration with Azure OpenAI for AI-powered insights
"""
import requests
from typing import Dict, Tuple, Optional
import json

class AzureAIService:
    """Service for Azure AI Foundry integration"""
    
    def __init__(self, endpoint: str, api_key: str, deployment_name: str, api_version: str = '2024-02-15-preview'):
        self.endpoint = endpoint.rstrip('/')
        self.api_key = api_key
        self.deployment_name = deployment_name
        self.api_version = api_version
    
    def test_connection(self) -> Tuple[bool, str]:
        """Test connection to Azure AI"""
        try:
            # Test with a simple completion request
            success, response, error = self.generate_completion(
                prompt="Say 'Hello' if you can hear me.",
                max_tokens=10
            )
            
            if success:
                return True, f"Connection successful! Response: {response}"
            else:
                return False, f"Connection failed: {error}"
        
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def generate_completion(self, prompt: str, max_tokens: int = 500, temperature: float = 0.7) -> Tuple[bool, str, str]:
        """Generate AI completion"""
        try:
            url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
            
            headers = {
                'Content-Type': 'application/json',
                'api-key': self.api_key
            }
            
            payload = {
                'messages': [
                    {'role': 'user', 'content': prompt}
                ],
                'max_tokens': max_tokens,
                'temperature': temperature
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                content = data['choices'][0]['message']['content']
                return True, content, ""
            else:
                return False, "", f"API error: {response.status_code} - {response.text}"
        
        except requests.exceptions.Timeout:
            return False, "", "Request timeout"
        except requests.exceptions.ConnectionError:
            return False, "", "Connection error. Check endpoint URL."
        except Exception as e:
            return False, "", f"Error: {str(e)}"
    
    def enhance_recommendations(self, gaps: list, signals: dict, customer_name: str) -> Tuple[bool, list, str]:
        """Use AI to enhance recommendations"""
        try:
            prompt = f"""You are a cybersecurity consultant analyzing a Strategic Business Review for {customer_name}.

Given the following gaps and metrics, provide 3-5 enhanced, specific recommendations:

Gaps identified:
{json.dumps(gaps, indent=2)}

Current metrics:
{json.dumps(signals, indent=2)}

Provide recommendations in JSON format:
[
  {{
    "title": "Recommendation title",
    "priority": "Critical|High|Medium|Low",
    "category": "Security|Infrastructure|Training|Process",
    "rationale": "Why this is needed",
    "expected_impact": "What will improve",
    "estimated_savings": "Cost savings or risk reduction"
  }}
]

Return only valid JSON, no other text."""

            success, response, error = self.generate_completion(prompt, max_tokens=2000, temperature=0.7)
            
            if success:
                # Try to parse JSON from response
                try:
                    # Find JSON in response
                    start = response.find('[')
                    end = response.rfind(']') + 1
                    if start >= 0 and end > start:
                        json_str = response[start:end]
                        recommendations = json.loads(json_str)
                        return True, recommendations, "AI recommendations generated successfully"
                    else:
                        return False, [], "Could not find valid JSON in AI response"
                except json.JSONDecodeError as e:
                    return False, [], f"JSON parse error: {str(e)}"
            else:
                return False, [], error
        
        except Exception as e:
            return False, [], f"Error generating AI recommendations: {str(e)}"
    
    def generate_executive_summary(self, customer_name: str, overall_score: float, 
                                   gaps: list, recommendations: list) -> Tuple[bool, str, str]:
        """Generate AI-powered executive summary"""
        try:
            prompt = f"""Write a concise executive summary for {customer_name}'s Strategic Business Review.

Overall Security Score: {overall_score:.1f}%
Number of Gaps: {len(gaps)}
Top Recommendations: {len(recommendations)}

Key gaps:
{json.dumps(gaps[:3], indent=2)}

Write a 2-3 paragraph executive summary that:
1. Summarizes the current security posture
2. Highlights the most critical risks
3. Emphasizes the business impact
4. Provides a clear call to action

Keep it professional, concise, and business-focused."""

            success, response, error = self.generate_completion(prompt, max_tokens=500, temperature=0.7)
            
            if success:
                return True, response.strip(), "Executive summary generated"
            else:
                return False, "", error
        
        except Exception as e:
            return False, "", f"Error generating summary: {str(e)}"

