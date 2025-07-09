# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# add docstring to this module

import json
import random
from datetime import datetime
from typing import Dict, List, Any, Optional

from google.adk.tools import ToolContext

# Initialize the client for dynamic question generation
# This will be set up lazily when needed to avoid import issues
genai_client = None

def _get_genai_client():
    """Lazy initialization of the genai client"""
    global genai_client
    if genai_client is None:
        try:
            import google.genai as genai
            genai_client = genai.Client()
        except ImportError:
            print("Warning: google-genai not available, falling back to hardcoded questions")
            genai_client = None
    return genai_client

# Topic definitions
TOPICS = {
    1: "Basic Syntax and Variables",
    2: "Control Flow and Conditionals", 
    3: "Loops and Iteration",
    4: "Lists and Basic Functions"
}

# Detailed topic content for dynamic question generation
TOPIC_CONTENT = {
    1: {
        "name": "Basic Syntax and Variables",
        "key_concepts": [
            "Python syntax basics and indentation rules",
            "Variable creation and naming conventions", 
            "Data types: strings, integers, floats, booleans",
            "Variable assignment and reassignment",
            "Print statements and basic input/output",
            "Comments using # symbol"
        ],
        "learning_objectives": [
            "Understand how to create and name variables properly",
            "Distinguish between different data types",
            "Use print() function for output",
            "Write clear comments in code"
        ]
    },
    2: {
        "name": "Control Flow and Conditionals",
        "key_concepts": [
            "If/elif/else statement structure",
            "Comparison operators (==, !=, <, >, <=, >=)",
            "Logical operators (and, or, not)",
            "Boolean expressions and evaluation",
            "Nested conditionals",
            "Indentation in conditional blocks"
        ],
        "learning_objectives": [
            "Write conditional statements to make decisions in code",
            "Use comparison and logical operators effectively",
            "Understand boolean logic and expressions",
            "Structure nested conditionals properly"
        ]
    },
    3: {
        "name": "Loops and Iteration",
        "key_concepts": [
            "For loops with ranges and sequences",
            "While loops and loop conditions",
            "Break and continue statements",
            "Nested loops and loop control",
            "Range function and its parameters",
            "Iterating over different data structures"
        ],
        "learning_objectives": [
            "Choose appropriate loop type for different scenarios",
            "Control loop execution with break and continue",
            "Write efficient loops that avoid infinite loops",
            "Use range() function effectively"
        ]
    },
    4: {
        "name": "Lists and Basic Functions",
        "key_concepts": [
            "Creating and initializing lists",
            "List indexing and slicing",
            "List methods (append, remove, pop, insert, etc.)",
            "Function definition with def keyword",
            "Parameters, arguments, and return values",
            "Function scope and local variables"
        ],
        "learning_objectives": [
            "Create and manipulate lists effectively",
            "Define functions with appropriate parameters",
            "Use return statements to output function results",
            "Understand variable scope in functions"
        ]
    }
}

# Quiz question pools for each topic (kept as fallback)
QUIZ_QUESTIONS = {
    1: [  # Basic Syntax and Variables
        {
            "question": "What is a variable in Python and how do you create one?",
            "key_concepts": ["variable", "assignment", "equals sign", "name", "value"],
            "sample_answer": "A variable is a name that stores a value. You create one by using the assignment operator (=), like: name = 'John'"
        },
        {
            "question": "What are the main data types in Python? Give an example of each.",
            "key_concepts": ["string", "integer", "float", "boolean", "str", "int", "bool"],
            "sample_answer": "String ('hello'), Integer (42), Float (3.14), Boolean (True/False)"
        },
        {
            "question": "How do you display output in Python?",
            "key_concepts": ["print", "output", "display", "console"],
            "sample_answer": "Use the print() function, like: print('Hello World')"
        },
        {
            "question": "What are Python's rules for variable naming?",
            "key_concepts": ["letters", "underscore", "numbers", "start", "keywords"],
            "sample_answer": "Start with letter or underscore, can contain letters/numbers/underscores, no spaces or special characters, can't be keywords"
        },
        {
            "question": "How do you add comments to Python code?",
            "key_concepts": ["hash", "#", "comment", "explain"],
            "sample_answer": "Use # for single line comments, like: # This is a comment"
        }
    ],
    2: [  # Control Flow and Conditionals
        {
            "question": "How do you write an if statement in Python?",
            "key_concepts": ["if", "condition", "colon", "indentation", "true"],
            "sample_answer": "Use 'if condition:' followed by indented code block that runs when condition is True"
        },
        {
            "question": "What's the difference between == and = in Python?",
            "key_concepts": ["comparison", "assignment", "equality", "operator"],
            "sample_answer": "== compares values for equality, = assigns a value to a variable"
        },
        {
            "question": "How do you check multiple conditions in Python?",
            "key_concepts": ["elif", "else", "and", "or", "multiple"],
            "sample_answer": "Use elif for additional conditions, else for default case, and/or for combining conditions"
        },
        {
            "question": "What are comparison operators in Python?",
            "key_concepts": ["==", "!=", "<", ">", "<=", ">=", "compare"],
            "sample_answer": "==, !=, <, >, <=, >= for comparing values"
        },
        {
            "question": "How do logical operators work in Python?",
            "key_concepts": ["and", "or", "not", "boolean", "logic"],
            "sample_answer": "'and' requires both conditions true, 'or' requires at least one true, 'not' reverses the boolean"
        }
    ],
    3: [  # Loops and Iteration
        {
            "question": "What's the difference between for loops and while loops?",
            "key_concepts": ["for", "while", "iteration", "condition", "sequence"],
            "sample_answer": "For loops iterate over sequences/ranges, while loops continue as long as a condition is True"
        },
        {
            "question": "How do you create a for loop that counts from 1 to 5?",
            "key_concepts": ["for", "range", "1", "5", "loop"],
            "sample_answer": "for i in range(1, 6): (range goes from 1 to 5 inclusive)"
        },
        {
            "question": "What do 'break' and 'continue' do in loops?",
            "key_concepts": ["break", "continue", "exit", "skip", "loop"],
            "sample_answer": "'break' exits the loop completely, 'continue' skips the rest of current iteration and goes to next"
        },
        {
            "question": "How do you loop through a list in Python?",
            "key_concepts": ["for", "list", "iterate", "items", "elements"],
            "sample_answer": "for item in my_list: or for i in range(len(my_list)):"
        },
        {
            "question": "When would you use a while loop instead of a for loop?",
            "key_concepts": ["while", "condition", "unknown", "iterations", "input"],
            "sample_answer": "When you don't know how many iterations you need, like waiting for user input or until a condition changes"
        }
    ],
    4: [  # Lists and Basic Functions
        {
            "question": "How do you create a list in Python and add items to it?",
            "key_concepts": ["list", "square brackets", "append", "add", "items"],
            "sample_answer": "Create with square brackets: my_list = [], add items with append(): my_list.append('item')"
        },
        {
            "question": "How do you access specific items in a list?",
            "key_concepts": ["index", "bracket", "position", "access", "zero"],
            "sample_answer": "Use square brackets with index: my_list[0] for first item (Python uses zero-based indexing)"
        },
        {
            "question": "How do you define a function in Python?",
            "key_concepts": ["def", "function", "parameters", "return", "colon"],
            "sample_answer": "Use 'def function_name(parameters):' followed by indented function body"
        },
        {
            "question": "What are some common list methods?",
            "key_concepts": ["append", "remove", "pop", "insert", "methods"],
            "sample_answer": "append() adds items, remove() deletes by value, pop() removes by index, insert() adds at position"
        },
        {
            "question": "How do you return a value from a function?",
            "key_concepts": ["return", "value", "function", "output"],
            "sample_answer": "Use the 'return' statement followed by the value: return result"
        }
    ]
}


def analyze_student_performance(tool_context: ToolContext) -> dict:
    """
    Analyze student's overall performance to determine appropriate difficulty level
    and identify learning gaps that need reinforcement.
    """
    # Use state for persistent data across sessions
    quiz_history = tool_context.state.get("quiz_history", {})
    
    if not quiz_history:
        return {
            "difficulty_level": "beginner",
            "average_score": 0,
            "learning_gaps": [],
            "strong_areas": [],
            "total_quizzes": 0
        }
    
    all_scores = []
    concept_performance = {}
    recent_mistakes = []
    
    for topic_num, quizzes in quiz_history.items():
        for quiz in quizzes[-3:]:  # Look at last 3 quizzes per topic
            all_scores.append(quiz.get("score", 0))
            
            # Track concept-level performance
            for result in quiz.get("results", []):
                question = result.get("question", "")
                correct = result.get("correct", False)
                
                if not correct:
                    recent_mistakes.append({
                        "topic": int(topic_num),
                        "question": question,
                        "student_answer": result.get("student_answer", ""),
                        "date": quiz.get("date", "")
                    })
    
    average_score = sum(all_scores) / len(all_scores) if all_scores else 0
    
    # Determine difficulty level
    if average_score >= 85:
        difficulty_level = "advanced"
    elif average_score >= 70:
        difficulty_level = "intermediate"
    else:
        difficulty_level = "beginner"
    
    return {
        "difficulty_level": difficulty_level,
        "average_score": average_score,
        "recent_mistakes": recent_mistakes[-5:],  # Last 5 mistakes
        "total_quizzes": len(all_scores),
        "score_trend": "improving" if len(all_scores) >= 2 and all_scores[-1] > all_scores[-2] else "stable"
    }


def generate_adaptive_questions(tool_context: ToolContext, topic_number: int, num_questions: int = 3) -> dict:
    """
    Generate quiz questions dynamically using the model, adapted to student's
    learning level, performance history, and specific areas needing reinforcement.
    """
    if topic_number not in TOPICS:
        return {"error": f"Invalid topic number: {topic_number}"}
    
    # Analyze student performance
    performance = analyze_student_performance(tool_context)
    topic_content = TOPIC_CONTENT.get(topic_number, {})
    
    # Build context for question generation
    context_prompt = f"""
    You are generating {num_questions} quiz questions for a Python tutoring system.
    
    TOPIC: {topic_content.get('name', TOPICS[topic_number])}
    
    KEY CONCEPTS TO COVER:
    {chr(10).join('- ' + concept for concept in topic_content.get('key_concepts', []))}
    
    LEARNING OBJECTIVES:
    {chr(10).join('- ' + obj for obj in topic_content.get('learning_objectives', []))}
    
    STUDENT PERFORMANCE ANALYSIS:
    - Difficulty Level: {performance['difficulty_level']}
    - Average Score: {performance['average_score']:.1f}%
    - Total Quizzes Taken: {performance['total_quizzes']}
    
    RECENT MISTAKES TO ADDRESS:
    {chr(10).join('- ' + mistake['question'] + ' (Answer: ' + mistake['student_answer'] + ')' for mistake in performance.get('recent_mistakes', [])[:3])}
    
    QUESTION GENERATION GUIDELINES:
    1. Generate {num_questions} unique questions that test understanding of the key concepts
    2. Adjust difficulty to {performance['difficulty_level']} level
    3. If there are recent mistakes, create 1-2 questions that reinforce those concepts
    4. Include a mix of conceptual understanding and practical application
    5. Questions should allow for natural language answers (no exact code syntax required)
    6. Each question should focus on 2-3 key concepts maximum
    
    FORMAT YOUR RESPONSE AS JSON:
    {{
        "questions": [
            {{
                "question": "Question text here",
                "key_concepts": ["concept1", "concept2"],
                "difficulty": "beginner|intermediate|advanced",
                "question_type": "conceptual|practical|application",
                "addresses_previous_mistake": true/false
            }}
        ]
    }}
    """
    
    try:
        # Generate questions using the model
        client = _get_genai_client()
        if client is None:
            # Fallback if genai client is not available
            return _generate_fallback_questions(topic_number, num_questions)
        
        response = client.models.generate_content(
            model="gemini-2.0-flash", 
            contents=context_prompt
        )
        
        # Parse the JSON response
        questions_data = json.loads(response.text)
        questions = questions_data.get("questions", [])
        
        if len(questions) < num_questions:
            # Fallback to hardcoded questions if generation fails
            return _generate_fallback_questions(topic_number, num_questions)
        
        return {
            "success": True,
            "questions": questions,
            "generation_method": "dynamic",
            "difficulty_level": performance['difficulty_level']
        }
        
    except Exception as e:
        # Fallback to hardcoded questions if generation fails
        print(f"Dynamic question generation failed: {e}")
        return _generate_fallback_questions(topic_number, num_questions)


def _generate_fallback_questions(topic_number: int, num_questions: int) -> dict:
    """Fallback to hardcoded questions if dynamic generation fails"""
    available_questions = QUIZ_QUESTIONS.get(topic_number, [])
    if len(available_questions) < num_questions:
        num_questions = len(available_questions)
    
    selected_questions = random.sample(available_questions, num_questions)
    
    # Convert to new format
    formatted_questions = []
    for q in selected_questions:
        formatted_questions.append({
            "question": q["question"],
            "key_concepts": q.get("key_concepts", []),
            "difficulty": "intermediate",
            "question_type": "conceptual",
            "addresses_previous_mistake": False
        })
    
    return {
        "success": True,
        "questions": formatted_questions,
        "generation_method": "fallback",
        "difficulty_level": "intermediate"
    }


def evaluate_answer_with_llm(tool_context: ToolContext, student_answer: str, question_data: dict) -> dict:
    """
    Use the model to evaluate student answers with sophisticated understanding
    of concepts rather than simple keyword matching.
    """
    evaluation_prompt = f"""
    You are evaluating a student's answer to a Python programming question.
    
    QUESTION: {question_data['question']}
    STUDENT ANSWER: {student_answer}
    
    KEY CONCEPTS THIS QUESTION TESTS:
    {', '.join(question_data.get('key_concepts', []))}
    
    EVALUATION CRITERIA:
    1. Does the student demonstrate understanding of the core concepts?
    2. Is the explanation conceptually correct, even if not perfectly worded?
    3. Are there any misconceptions evident in the answer?
    4. What specific feedback would help the student improve?
    
    RESPOND IN JSON FORMAT:
    {{
        "correct": true/false,
        "confidence": 0.0-1.0,
        "concepts_understood": ["concept1", "concept2"],
        "misconceptions": ["misconception1"],
        "feedback": "Detailed feedback explaining why the answer is correct/incorrect",
        "suggestions": "Specific suggestions for improvement"
    }}
    
    Be generous with partial credit for conceptual understanding, even if the wording isn't perfect.
    """
    
    try:
        client = _get_genai_client()
        if client is None:
            # Fallback if genai client is not available
            return _evaluate_with_keywords(student_answer, question_data)
        
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=evaluation_prompt
        )
        evaluation = json.loads(response.text)
        
        return {
            "correct": evaluation.get("correct", False),
            "confidence": evaluation.get("confidence", 0.5),
            "feedback": evaluation.get("feedback", "Unable to evaluate answer."),
            "suggestions": evaluation.get("suggestions", ""),
            "concepts_understood": evaluation.get("concepts_understood", []),
            "misconceptions": evaluation.get("misconceptions", []),
            "evaluation_method": "llm"
        }
        
    except Exception as e:
        # Fallback to keyword matching if LLM evaluation fails
        return _evaluate_with_keywords(student_answer, question_data)


def _evaluate_with_keywords(student_answer: str, question_data: dict) -> dict:
    """Fallback keyword-based evaluation"""
    key_concepts = question_data.get("key_concepts", [])
    student_lower = student_answer.lower()
    
    concepts_found = sum(1 for concept in key_concepts if concept.lower() in student_lower)
    concept_threshold = max(1, len(key_concepts) // 2)
    
    is_correct = concepts_found >= concept_threshold
    
    return {
        "correct": is_correct,
        "confidence": concepts_found / len(key_concepts) if key_concepts else 0.5,
        "feedback": f"Found {concepts_found} out of {len(key_concepts)} key concepts in your answer.",
        "suggestions": "Try to include more of the key concepts in your explanation.",
        "concepts_understood": [],
        "misconceptions": [],
        "evaluation_method": "keyword"
    }


# ----- Example of a Function tool -----
def get_current_date() -> dict:
    """
    Get the current date in the format YYYY-MM-DD
    """
    return {"current_date": datetime.now().strftime("%Y-%m-%d")}


def get_student_progress(tool_context: ToolContext) -> dict:
    """
    Check the student's current topic and past quiz performance.
    Returns progress information including current topic and areas needing review.
    """
    # Get current topic from persistent state (default to topic 1)
    current_topic = tool_context.state.get("current_topic", 1)
    
    # Get quiz history from persistent state
    quiz_history = tool_context.state.get("quiz_history", {})
    
    # Find questions that need review (scored incorrectly)
    review_needed = {}
    for topic_num, quizzes in quiz_history.items():
        topic_num = int(topic_num)
        incorrect_questions = []
        
        for quiz in quizzes:
            for i, result in enumerate(quiz.get("results", [])):
                if not result.get("correct", False):
                    incorrect_questions.append({
                        "question": result.get("question", ""),
                        "student_answer": result.get("student_answer", ""),
                        "date": quiz.get("date", "")
                    })
        
        if incorrect_questions:
            review_needed[topic_num] = incorrect_questions
    
    # Calculate overall progress
    total_topics = len(TOPICS)
    topics_completed = len([t for t in range(1, current_topic) if str(t) not in review_needed])
    progress_percentage = (topics_completed / total_topics) * 100
    
    # Get performance analysis
    performance = analyze_student_performance(tool_context)
    
    return {
        "current_topic": current_topic,
        "current_topic_name": TOPICS.get(current_topic, "Unknown"),
        "total_topics": total_topics,
        "progress_percentage": progress_percentage,
        "review_needed": review_needed,
        "quiz_history_summary": {
            str(topic): len(quizzes) for topic, quizzes in quiz_history.items()
        },
        "performance_analysis": performance
    }


def generate_topic_quiz(tool_context: ToolContext, topic_number: int, num_questions: int = 3, use_dynamic: bool = True) -> dict:
    """
    Generate a quiz for a specific topic with the specified number of questions.
    Now supports both dynamic generation and fallback to hardcoded questions.
    """
    if topic_number not in TOPICS:
        return {"error": f"Invalid topic number: {topic_number}"}
    
    # Try dynamic generation first if enabled
    if use_dynamic:
        questions_result = generate_adaptive_questions(tool_context, topic_number, num_questions)
    else:
        questions_result = _generate_fallback_questions(topic_number, num_questions)
    
    if not questions_result.get("success"):
        return {"error": "Failed to generate quiz questions"}
    
    questions = questions_result["questions"]
    
    # Create quiz structure
    quiz_data = {
        "topic_number": topic_number,
        "topic_name": TOPICS[topic_number],
        "questions": questions,
        "current_question": 0,
        "total_questions": len(questions),
        "results": [],
        "generation_method": questions_result.get("generation_method", "unknown"),
        "difficulty_level": questions_result.get("difficulty_level", "intermediate")
    }
    
    # Store in session state (temporary for current quiz)
    tool_context.state["current_quiz"] = quiz_data
    tool_context.state["quiz_active"] = True
    
    return {
        "topic_number": topic_number,
        "topic_name": TOPICS[topic_number], 
        "total_questions": len(questions),
        "first_question": questions[0]["question"] if questions else None,
        "quiz_started": True,
        "generation_method": questions_result.get("generation_method"),
        "difficulty_level": questions_result.get("difficulty_level")
    }


def evaluate_quiz_answer(tool_context: ToolContext, student_answer: str, use_llm_evaluation: bool = True) -> dict:
    """
    Evaluate a student's natural language answer to the current quiz question.
    Now supports both LLM-based evaluation and fallback keyword matching.
    Automatically saves quiz results and advances topics when quiz is complete.
    """
    # Get current quiz from session state
    current_quiz = tool_context.state.get("current_quiz")
    if not current_quiz:
        return {"error": "No active quiz found"}
    
    current_q_index = current_quiz["current_question"]
    if current_q_index >= len(current_quiz["questions"]):
        return {"error": "No more questions in quiz"}
    
    current_question = current_quiz["questions"][current_q_index]
    
    # Use LLM evaluation if enabled
    if use_llm_evaluation:
        evaluation = evaluate_answer_with_llm(tool_context, student_answer, current_question)
    else:
        evaluation = _evaluate_with_keywords(student_answer, current_question)
    
    # Store result with enhanced data
    result = {
        "question": current_question["question"],
        "student_answer": student_answer,
        "correct": evaluation["correct"],
        "confidence": evaluation.get("confidence", 0.5),
        "feedback": evaluation.get("feedback", ""),
        "suggestions": evaluation.get("suggestions", ""),
        "concepts_understood": evaluation.get("concepts_understood", []),
        "misconceptions": evaluation.get("misconceptions", []),
        "question_data": current_question,
        "evaluation_method": evaluation.get("evaluation_method", "unknown")
    }
    
    current_quiz["results"].append(result)
    current_quiz["current_question"] += 1
    
    # Update session state
    tool_context.state["current_quiz"] = current_quiz
    
    # Check if quiz is complete
    quiz_complete = current_quiz["current_question"] >= current_quiz["total_questions"]
    next_question = None
    
    if not quiz_complete:
        next_question = current_quiz["questions"][current_quiz["current_question"]]["question"]
    else:
        # Quiz is complete - automatically store results and check for topic advancement
        tool_context.state["quiz_active"] = False
        
        # Automatically save quiz results
        storage_result = _auto_store_quiz_results(tool_context)
        
        return {
            "correct": evaluation["correct"],
            "confidence": evaluation.get("confidence", 0.5),
            "feedback": evaluation.get("feedback", ""),
            "suggestions": evaluation.get("suggestions", ""),
            "quiz_complete": True,
            "next_question": None,
            "question_number": current_q_index + 1,
            "total_questions": current_quiz["total_questions"],
            "concepts_understood": evaluation.get("concepts_understood", []),
            "misconceptions": evaluation.get("misconceptions", []),
            "quiz_results": storage_result  # Include the automatic storage results
        }
    
    return {
        "correct": evaluation["correct"],
        "confidence": evaluation.get("confidence", 0.5),
        "feedback": evaluation.get("feedback", ""),
        "suggestions": evaluation.get("suggestions", ""),
        "quiz_complete": quiz_complete,
        "next_question": next_question,
        "question_number": current_q_index + 1,
        "total_questions": current_quiz["total_questions"],
        "concepts_understood": evaluation.get("concepts_understood", []),
        "misconceptions": evaluation.get("misconceptions", [])
    }


def _auto_store_quiz_results(tool_context: ToolContext) -> dict:
    """
    Internal function to automatically store quiz results when a quiz is completed.
    This ensures quiz results are always saved and topics advance correctly.
    """
    # Get completed quiz from session state
    current_quiz = tool_context.state.get("current_quiz")
    if not current_quiz:
        return {"error": "No completed quiz to store"}
    
    topic_number = current_quiz["topic_number"]
    
    # Calculate quiz score and enhanced analytics
    correct_answers = sum(1 for result in current_quiz["results"] if result["correct"])
    total_questions = len(current_quiz["results"])
    score_percentage = (correct_answers / total_questions * 100) if total_questions > 0 else 0
    
    # Calculate average confidence
    avg_confidence = sum(result.get("confidence", 0.5) for result in current_quiz["results"]) / total_questions if total_questions > 0 else 0
    
    # Collect misconceptions and understood concepts
    all_misconceptions = []
    all_understood_concepts = []
    
    for result in current_quiz["results"]:
        all_misconceptions.extend(result.get("misconceptions", []))
        all_understood_concepts.extend(result.get("concepts_understood", []))
    
    # Create enhanced quiz record
    quiz_record = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic_number": topic_number,
        "topic_name": TOPICS[topic_number],
        "score": score_percentage,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "average_confidence": avg_confidence,
        "generation_method": current_quiz.get("generation_method", "unknown"),
        "difficulty_level": current_quiz.get("difficulty_level", "intermediate"),
        "misconceptions": list(set(all_misconceptions)),  # Remove duplicates
        "understood_concepts": list(set(all_understood_concepts)),
        "results": current_quiz["results"]
    }
    
    # Get existing quiz history from persistent state
    quiz_history = tool_context.state.get("quiz_history", {})
    topic_key = str(topic_number)
    
    if topic_key not in quiz_history:
        quiz_history[topic_key] = []
    
    quiz_history[topic_key].append(quiz_record)
    
    # Update persistent state with quiz history
    tool_context.state["quiz_history"] = quiz_history
    
    # Update current topic if student passed (70% or better with reasonable confidence)
    passing_score = 70
    min_confidence = 0.6
    passed = score_percentage >= passing_score and avg_confidence >= min_confidence
    
    if passed:
        current_topic = tool_context.state.get("current_topic", 1)
        if topic_number == current_topic and current_topic < len(TOPICS):
            new_topic = current_topic + 1
            tool_context.state["current_topic"] = new_topic
            print(f"🎉 Student passed Topic {topic_number}! Advanced to Topic {new_topic}")
    
    # Clear session state
    tool_context.state["current_quiz"] = None
    tool_context.state["quiz_active"] = False
    
    return {
        "stored": True,
        "topic_number": topic_number,
        "topic_name": TOPICS[topic_number],
        "score_percentage": score_percentage,
        "correct_answers": correct_answers,
        "total_questions": total_questions,
        "average_confidence": avg_confidence,
        "passed": passed,
        "next_topic": tool_context.state.get("current_topic", topic_number),
        "generation_method": current_quiz.get("generation_method", "unknown"),
        "difficulty_level": current_quiz.get("difficulty_level", "intermediate"),
        "misconceptions_identified": len(set(all_misconceptions)),
        "concepts_mastered": len(set(all_understood_concepts))
    }


def store_quiz_results(tool_context: ToolContext) -> dict:
    """
    Manually store completed quiz results in persistent state and update progress.
    Note: Quiz results are now automatically stored when a quiz completes,
    but this function remains available for manual control if needed.
    """
    return _auto_store_quiz_results(tool_context)
