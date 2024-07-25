import argparse
import random 
import json 
import pydantic


class Question:
    def __init__(self, question, answers, correct_answer):
        self.question = question
        self.answers = answers
        self.correct_answer = correct_answer

    def load_questions(file_path):
        with open(file_path, 'r') as f:
            questions_data = json.load(f)
        questions = []
        for item in questions_data:
            question = Question(
                item['question'],
                item['answers'],
                item['correct_answer']
            )
            questions.append(question)
        return questions

    def get_random_question(questions):
        return random.choice(questions)

    def display(self):
        print(f"Question: {self.question}")
        for i, answer in enumerate(self.answers):
            print(f"{i + 1}. {answer}")
        
        while True:
            user_input = input("Choose the number of your answer: ")
            if user_input.strip() == "":  # אם הקלט ריק
                print("No input provided. Please enter a number.")
                continue
            
            try:
                answer_index = int(user_input) - 1
                if 0 <= answer_index < len(self.answers):
                    return answer_index
                else:
                    print("Invalid choice. Please choose a valid number from the list.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    def is_correct(self, answer_index):
        return self.answers[answer_index] == self.correct_answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trivia Game")
    parser.add_argument("file_path", help="Path to the JSON file containing questions")
    args = parser.parse_args()

    questions = Question.load_questions(args.file_path)
    
    num_players = int(input("Enter number of players: "))
    player_names = []
    for i in range(num_players):
        name = input(f"Enter name for player {i + 1}: ")
        player_names.append(name)
        
    scores = [0] * num_players
    player_turn = 0
    current_question = Question.get_random_question(questions) 

    while questions:
        current_player = player_names[player_turn]
        print(f"\n{current_player}'s turn!")

        print("\nCurrent Question:")
        answer_index = current_question.display()

        if current_question.is_correct(answer_index):
            print("Correct!")
            scores[player_turn] += 1
            questions.remove(current_question) 
            if questions: 
                current_question = Question.get_random_question(questions) 
        else:
            print("Wrong! The question will remain.")

        player_turn = (player_turn + 1) % num_players

    print("\nGame Over!")
    max_score = max(scores)
    winners = [player_names[i] for i, score in enumerate(scores) if score == max_score]

    if len(winners) > 1:
        print(f"It's a tie! The winners are: {', '.join(winners)} with {max_score} points!")
    else:
        winner_index = scores.index(max_score)
        print(f"The winner is {player_names[winner_index]} with {scores[winner_index]} points!")
        
        
        
    
#       python game.py questions.json      (command to run the game in the terminal)    

