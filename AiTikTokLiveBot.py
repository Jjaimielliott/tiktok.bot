"""
AI-Powered TikTok Live Bot
Uses Claude AI to have natural conversations with viewers
"""
from TikTokLive import TikTokLiveClient
from TikTokLive.events import ConnectEvent, CommentEvent
import asyncio
import random
from datetime import datetime
from playwright.async_api import async_playwright
import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

class AiTikTokLiveBot:
    def __init__(self, username, anthropic_apia_key=None):
        """
       Initialize AI-powered bot

       Args:
           username: TikTok username to monitor
           ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
       """

        self.client = TikTokLiveClient(unique_id=f"@{nxble6}")
        self.username = username

        #claude ai setup
        self.anthropic_api_key:
        if not self.anthropic_api_key:
            print("⚠️  No API key found. Set ANTHROPIC_API_KEY environment variable")
            print("   Get your key at: https://console.anthropic.com/")
        self.claude = anthropic.Anthropic(api_key=self.anthropic_api_key) if self.anthropic_api_key else None

        # Bot personality and context
        self.streamer_name = "nxble"  # CUSTOMIZE THIS
        self.stream_topic = "gaming"  # CUSTOMIZE: gaming, art, music, chatting, etc.
        self.discord_link = "https://discord.gg/Vx7dTKNhN6"  # CUSTOMIZE THIS
        self.other_socials = {
            "instagram": "@nxble06",
            "youtube": "@nxble6",

        }

        # Bot settings
        self.browser = None
        self.page = None
        self.is_logged_in = False
        self.comment_queue = asyncio.Queue()
        self.last_comment_time = None
        self.min_comment_delay = 12  # Minimum seconds between comments
        self.reminder_interval = 240  # 4 minutes between reminders

        # Conversation memory (last 10 messages for context)
        self.conversation_history = []
        self.max_history = 10

        # Stats tracking
        self.total_comments = 0
        self.ai_responses = 0

        # Comment queue to avoid spam
        self.comment_queue = asyncio.Queue()
        self.last_comment_time = None
        self.min_comment_delay = 10  # Minimum 10 seconds between comments

        self.auto_responses = {
            "discord": f"Join our Discord community: {self.discord_link} 🎮",
            "link": f"Discord link: {self.discord_link} 💬",
            "hi": ["Hey! 👋", "Hello! Welcome! 🎉", "Hi there! 😊"],
            "hello": ["Hey! 👋", "Hello! Welcome! 🎉", "Hi there! 😊"],
        }

        self.client.add_listener("connect", self.on_connect)
        self.client.add_listener("comment", self.on_comment)

    def build_system_prompt (self):#
        """Create the AI Personality"""
        return f"""You are a friendly, engaging chat bot {self.streamer}'s Tiktok live stream.
    
STREAM CONVEXT: 
    - Streamer: {self.streamer_name}
    - Content: {self.stream_topic}
    - Discord: {self.discord_link}
    - Instagram: {self.other_socials.get('instagram', 'N/A')}
    - YouTube: {self.other_socials.get('youtube', 'N/A')}
    
YOUR ROLE:
- Engage naturally with viewers
- Answer questions about the stream, streamer, and content
- Encourage people to like, follow, and join Discord (but not too pushy!)
- Be friendly, welcoming, and fun
- Keep responses SHORT (1-2 sentences max, under 150 characters ideal for TikTok)
- Use emojis occasionally but don't overdo it
- Be conversational and natural, not robotic

RESPONSE GUIDELINES:
- Keep it brief and casual
- Match the energy of the chat
- If someone asks about Discord/socials, share the links
- Welcome new viewers warmly
- Thank people for likes and follows
- Answer questions about {self.stream_topic}
- If you don't know something, be honest but friendly

AVOID:
- Long explanations
- Being too formal or corporate
- Spam or repetitive messages
- Controversial topics
- Negative or rude responses"""

async def setup_browser(self:
    """setup Playwright browser for sending comments"""
    print("Setting up browser...")
    playwright = await async_playwright().start()

