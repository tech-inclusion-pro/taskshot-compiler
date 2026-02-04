"""
TaskShot AI Client - Multi-provider alt text generation
Supports: Local Ollama, OpenAI, Anthropic, and custom APIs
"""

import base64
import requests
from pathlib import Path


class OllamaClient:
    """Client for AI APIs to generate alt text for screenshots"""

    def __init__(self, settings):
        self.settings = settings

    def generate_alt_text(self, image_path):
        """
        Generate alt text for an image using the configured AI provider.

        Args:
            image_path: Path to the screenshot image

        Returns:
            Generated alt text string, or fallback text on failure
        """
        # Check if AI is enabled
        if not self.settings.get('ai_enabled', True):
            return self._fallback_alt_text(image_path)

        # Get the AI provider
        provider = self.settings.get('ai_provider', 'ollama')

        if provider == 'ollama':
            return self._generate_ollama(image_path)
        elif provider == 'openai':
            return self._generate_openai(image_path)
        elif provider == 'anthropic':
            return self._generate_anthropic(image_path)
        elif provider == 'custom':
            return self._generate_custom(image_path)
        else:
            return self._fallback_alt_text(image_path)

    def _generate_ollama(self, image_path):
        """Generate alt text using local Ollama"""
        server_url = self.settings.get('ollama_url', 'http://localhost:11434')
        model = self.settings.get('ollama_model', 'llava:7b')

        try:
            image_data = self._encode_image(image_path)
            if not image_data:
                return self._fallback_alt_text(image_path)

            prompt = (
                "Describe this screenshot in 1-2 sentences for someone using a screen reader. "
                "Focus on the action being taken and UI elements visible. "
                "Be concise and specific. Do not start with 'This screenshot shows'."
            )

            response = requests.post(
                f"{server_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "images": [image_data],
                    "stream": False,
                    "options": {
                        "temperature": 0.3,
                        "num_predict": 100
                    }
                },
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                alt_text = result.get('response', '').strip()
                if alt_text:
                    return alt_text

            return self._fallback_alt_text(image_path)

        except Exception as e:
            print(f"Ollama error: {e}")
            return self._fallback_alt_text(image_path)

    def _generate_openai(self, image_path):
        """Generate alt text using OpenAI API"""
        api_key = self.settings.get('openai_api_key', '')
        model = self.settings.get('openai_model', 'gpt-4o')

        if not api_key:
            return self._fallback_alt_text(image_path)

        try:
            image_data = self._encode_image(image_path)
            if not image_data:
                return self._fallback_alt_text(image_path)

            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe this screenshot in 1-2 sentences for someone using a screen reader. Focus on the action being taken and UI elements visible. Be concise and specific."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 100
            }

            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                alt_text = result['choices'][0]['message']['content'].strip()
                if alt_text:
                    return alt_text

            return self._fallback_alt_text(image_path)

        except Exception as e:
            print(f"OpenAI error: {e}")
            return self._fallback_alt_text(image_path)

    def _generate_anthropic(self, image_path):
        """Generate alt text using Anthropic API"""
        api_key = self.settings.get('anthropic_api_key', '')
        model = self.settings.get('anthropic_model', 'claude-sonnet-4-20250514')

        if not api_key:
            return self._fallback_alt_text(image_path)

        try:
            image_data = self._encode_image(image_path)
            if not image_data:
                return self._fallback_alt_text(image_path)

            headers = {
                "x-api-key": api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }

            payload = {
                "model": model,
                "max_tokens": 100,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_data
                                }
                            },
                            {
                                "type": "text",
                                "text": "Describe this screenshot in 1-2 sentences for someone using a screen reader. Focus on the action being taken and UI elements visible. Be concise and specific."
                            }
                        ]
                    }
                ]
            }

            response = requests.post(
                "https://api.anthropic.com/v1/messages",
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                alt_text = result['content'][0]['text'].strip()
                if alt_text:
                    return alt_text

            return self._fallback_alt_text(image_path)

        except Exception as e:
            print(f"Anthropic error: {e}")
            return self._fallback_alt_text(image_path)

    def _generate_custom(self, image_path):
        """Generate alt text using custom API endpoint"""
        api_url = self.settings.get('custom_api_url', '')
        api_key = self.settings.get('custom_api_key', '')
        model = self.settings.get('custom_model', '')

        if not api_url:
            return self._fallback_alt_text(image_path)

        try:
            image_data = self._encode_image(image_path)
            if not image_data:
                return self._fallback_alt_text(image_path)

            headers = {
                "Content-Type": "application/json"
            }
            if api_key:
                headers["Authorization"] = f"Bearer {api_key}"

            # Use OpenAI-compatible format (works with many providers)
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Describe this screenshot in 1-2 sentences for someone using a screen reader. Focus on the action being taken and UI elements visible. Be concise and specific."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 100
            }

            response = requests.post(
                api_url,
                headers=headers,
                json=payload,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                # Try OpenAI format first
                if 'choices' in result:
                    alt_text = result['choices'][0]['message']['content'].strip()
                # Try Anthropic format
                elif 'content' in result:
                    alt_text = result['content'][0]['text'].strip()
                # Try simple response format
                elif 'response' in result:
                    alt_text = result['response'].strip()
                else:
                    alt_text = ''

                if alt_text:
                    return alt_text

            return self._fallback_alt_text(image_path)

        except Exception as e:
            print(f"Custom API error: {e}")
            return self._fallback_alt_text(image_path)

    def _encode_image(self, image_path):
        """
        Encode an image file to base64.

        Args:
            image_path: Path to the image file

        Returns:
            Base64 encoded string or None on failure
        """
        try:
            path = Path(image_path)
            if not path.exists():
                return None

            with open(path, 'rb') as f:
                return base64.b64encode(f.read()).decode('utf-8')
        except Exception as e:
            print(f"Error encoding image: {e}")
            return None

    def _fallback_alt_text(self, image_path):
        """
        Generate fallback alt text when AI is unavailable.

        Args:
            image_path: Path to the screenshot image

        Returns:
            Fallback alt text string
        """
        try:
            # Try to extract step number from filename
            filename = Path(image_path).stem
            if 'screenshot_' in filename:
                parts = filename.split('_')
                if len(parts) >= 2:
                    step_num = int(parts[1])
                    return f"Screenshot showing tutorial step {step_num}"
        except Exception:
            pass

        return "Screenshot showing a step in the tutorial"

    def test_connection(self):
        """
        Test connection to the configured AI provider.

        Returns:
            Tuple of (success: bool, message: str, models: list)
        """
        provider = self.settings.get('ai_provider', 'ollama')

        if provider == 'ollama':
            return self._test_ollama()
        elif provider == 'openai':
            return self._test_openai()
        elif provider == 'anthropic':
            return self._test_anthropic()
        elif provider == 'custom':
            return self._test_custom()
        else:
            return False, "Unknown provider", []

    def _test_ollama(self):
        """Test Ollama connection"""
        server_url = self.settings.get('ollama_url', 'http://localhost:11434')

        try:
            response = requests.get(f"{server_url}/api/tags", timeout=5)

            if response.status_code == 200:
                data = response.json()
                models = [m.get('name', 'Unknown') for m in data.get('models', [])]
                return True, "Connected to Ollama successfully", models
            else:
                return False, f"Server returned status {response.status_code}", []

        except requests.exceptions.ConnectionError:
            return False, "Could not connect to Ollama server", []
        except requests.exceptions.Timeout:
            return False, "Connection timed out", []
        except Exception as e:
            return False, str(e), []

    def _test_openai(self):
        """Test OpenAI connection"""
        api_key = self.settings.get('openai_api_key', '')

        if not api_key:
            return False, "No API key configured", []

        try:
            headers = {"Authorization": f"Bearer {api_key}"}
            response = requests.get(
                "https://api.openai.com/v1/models",
                headers=headers,
                timeout=5
            )

            if response.status_code == 200:
                data = response.json()
                models = [m['id'] for m in data.get('data', []) if 'gpt' in m['id']][:5]
                return True, "Connected to OpenAI successfully", models
            elif response.status_code == 401:
                return False, "Invalid API key", []
            else:
                return False, f"Server returned status {response.status_code}", []

        except Exception as e:
            return False, str(e), []

    def _test_anthropic(self):
        """Test Anthropic connection"""
        api_key = self.settings.get('anthropic_api_key', '')

        if not api_key:
            return False, "No API key configured", []

        # Anthropic doesn't have a simple models endpoint, so we just verify the key format
        if api_key.startswith('sk-ant-'):
            return True, "API key format looks valid", ['claude-sonnet-4-20250514', 'claude-3-5-sonnet-20241022', 'claude-3-haiku-20240307']
        else:
            return False, "API key should start with 'sk-ant-'", []

    def _test_custom(self):
        """Test custom API connection"""
        api_url = self.settings.get('custom_api_url', '')

        if not api_url:
            return False, "No API URL configured", []

        try:
            response = requests.get(api_url.replace('/chat/completions', '/models'), timeout=5)
            if response.status_code == 200:
                return True, "Connected to custom API", []
            return True, "API URL appears valid", []
        except Exception:
            return True, "API URL configured (connection test skipped)", []

    def is_available(self):
        """
        Check if AI is available and configured.

        Returns:
            bool indicating if AI can be used for alt text
        """
        provider = self.settings.get('ai_provider', 'ollama')

        if provider == 'ollama':
            success, _, models = self._test_ollama()
            if not success:
                return False
            vision_models = ['llava', 'moondream', 'bakllava']
            for model in models:
                for vision_model in vision_models:
                    if vision_model in model.lower():
                        return True
            return False
        elif provider == 'openai':
            return bool(self.settings.get('openai_api_key', ''))
        elif provider == 'anthropic':
            return bool(self.settings.get('anthropic_api_key', ''))
        elif provider == 'custom':
            return bool(self.settings.get('custom_api_url', ''))

        return False

    def get_provider_name(self):
        """Get the display name of the current AI provider"""
        provider = self.settings.get('ai_provider', 'ollama')
        names = {
            'ollama': 'Local Ollama',
            'openai': 'OpenAI',
            'anthropic': 'Anthropic Claude',
            'custom': 'Custom API'
        }
        return names.get(provider, 'Unknown')
