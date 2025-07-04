#!/usr/bin/env python3
"""
Example usage of the enhanced Python Tutor Agent with dynamic quiz generation.

This script demonstrates the new capabilities:
- Dynamic question generation based on student performance
- LLM-based answer evaluation with detailed feedback
- Adaptive difficulty adjustment
- Personalized learning paths with mistake remediation
- Cross-session continuity with performance analytics
"""

import os
from google.adk.sessions import Session
from python_tutor.agent import root_agent

def main():
    """Demonstrate the enhanced Python tutor functionality"""
    
    # Create a session for the student
    session = Session(
        user_id="student_456",
        session_id="dynamic_learning_session_1"
    )
    
    print("=== Enhanced Python Tutor Demo ===")
    print("This demo showcases the NEW dynamic capabilities:")
    print("✨ Dynamic question generation based on student performance")
    print("🧠 LLM-powered answer evaluation with detailed feedback")
    print("📊 Adaptive difficulty adjustment (beginner/intermediate/advanced)")
    print("🔄 Personalized questions that address previous mistakes")
    print("📈 Cross-session performance analytics and continuity")
    print("🎯 Fresh, unique questions every time (no repetition)")
    print()
    
    # Simulate a first-time student interaction with dynamic features
    print("--- First Session: Dynamic Question Generation ---")
    
    # Student starts their learning journey
    messages = [
        "Hi! I'm completely new to Python programming and want to learn.",
        "Yes, I'd like to start learning about variables and basic syntax.",
        "A variable is like a box that can hold different things. You make one by typing a name and using equals.",
        "The types are words, numbers, decimal numbers, and true/false things.",
        "You use print() to show things on the screen.",
    ]
    
    print("🎯 The agent will now generate questions dynamically based on:")
    print("   - Student's beginner level")
    print("   - Topic content and learning objectives")
    print("   - No previous performance history (first-time student)")
    print()
    
    for i, message in enumerate(messages):
        print(f"Student: {message}")
        response = root_agent.run(message, session)
        print(f"Tutor: {response.content}")
        print()
        
        if i == 0:
            print("💡 The agent analyzes student performance (none yet) and sets difficulty to 'beginner'")
        elif i == 1:
            print("🎲 Dynamic quiz generation: Creating personalized questions for Topic 1")
        elif i >= 2:
            print("🤖 LLM evaluation: Understanding conceptual knowledge beyond keywords")
        
        print("-" * 60)
    
    print("\n--- Second Session: Adaptive Learning in Action ---")
    
    # Simulate student returning with some performance history
    new_session = Session(
        user_id="student_456", 
        session_id="dynamic_learning_session_2"
    )
    
    print("Student: Hi, I'm back to continue learning!")
    response = root_agent.run("Hi, I'm back to continue learning!", new_session)
    print(f"Tutor: {response.content}")
    print()
    
    print("🧠 The agent now has performance data and will:")
    print("   ✓ Analyze previous quiz results and difficulty level")
    print("   ✓ Generate questions targeting any weak areas")
    print("   ✓ Adjust difficulty based on performance trends")
    print("   ✓ Create fresh variations (never exact repeats)")
    print("   ✓ Provide detailed, personalized feedback")
    
    print("\n--- Advanced Student Simulation ---")
    
    # Simulate an advanced student to show difficulty adaptation
    advanced_session = Session(
        user_id="advanced_student_789",
        session_id="advanced_session_1"
    )
    
    # Simulate high-performing student responses
    advanced_messages = [
        "I have some Python experience and want to advance my skills.",
        "Variables are references to objects in memory. Python uses dynamic typing where variables can be reassigned to different types. You create them using assignment operators like =, +=, etc.",
    ]
    
    print("\n🚀 Advanced Student Example:")
    for message in advanced_messages:
        print(f"Advanced Student: {message}")
        response = root_agent.run(message, advanced_session)
        print(f"Tutor: {response.content}")
        print()
    
    print("⚡ For advanced students, the system will:")
    print("   • Generate more challenging, multi-concept questions")
    print("   • Focus on edge cases and best practices")
    print("   • Connect concepts across topics")
    print("   • Encourage critical thinking about trade-offs")
    
    print("\n--- Key Dynamic Features Demonstrated ---")
    print("🎯 DYNAMIC QUESTION GENERATION:")
    print("   • Questions adapt to student's demonstrated ability level")
    print("   • Fresh content every time - no memorization of answers")
    print("   • Targeted remediation of specific learning gaps")
    print("   • Contextual questions that build on previous learning")
    
    print("\n🧠 INTELLIGENT EVALUATION:")
    print("   • LLM understands conceptual knowledge vs. keyword matching")
    print("   • Identifies specific misconceptions and provides targeted feedback")
    print("   • Tracks confidence levels in student understanding")
    print("   • Generous partial credit for conceptual understanding")
    
    print("\n📊 ADAPTIVE DIFFICULTY:")
    print("   • Beginner: Simple, foundational questions with encouragement")
    print("   • Intermediate: Mixed conceptual and practical applications")
    print("   • Advanced: Complex scenarios, edge cases, best practices")
    
    print("\n🔄 PERSONALIZED LEARNING PATHS:")
    print("   • Cross-session memory of performance and learning gaps")
    print("   • Questions specifically address previous mistakes")
    print("   • Unique learning journey for each student")
    print("   • Builds coherent learning narrative over time")
    
    print("\n--- Technical Implementation ---")
    print("🛠️ ENHANCED TOOLS:")
    print("   • analyze_student_performance(): Comprehensive performance analytics")
    print("   • generate_adaptive_questions(): Dynamic, personalized question creation")
    print("   • evaluate_answer_with_llm(): Sophisticated concept-based evaluation")
    print("   • Enhanced data tracking: misconceptions, confidence, difficulty levels")
    
    print("\n🎨 FALLBACK SYSTEM:")
    print("   • Hybrid approach: Dynamic generation with hardcoded fallbacks")
    print("   • Graceful degradation if LLM generation fails")
    print("   • Ensures reliable operation in all scenarios")

if __name__ == "__main__":
    # Set up environment for demo
    os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
    
    main() 