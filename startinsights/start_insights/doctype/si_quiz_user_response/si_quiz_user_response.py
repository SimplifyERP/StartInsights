# Copyright (c) 2024, Suriya and contributors
# For license information, please see license.txt
import frappe
from frappe.model.document import Document

class SIQuizUserResponse(Document):
    def validate(self):
        # Mapping of user response options to their textual representation
        option_map = {
            1: "First Option",
            2: "Second Option",
            3: "Third Option",
            4: "Fourth Option",
            5: "Fifth Option",
            6: "Sixth Option"
        }

        if self.quiz_completed == 1:
            # Fetch all score cards based on customer group and quiz name
            score_cards = frappe.db.get_all("Score Card", filters={"customer_group": self.customer_group, "quiz_name": self.quiz_name}, fields=["*"])
            match_found = False

            for score_card in score_cards:
                # Fetch entries from Score Card Table
                score_card_table_entries = frappe.db.get_all("Score Card Table", filters={"parent": score_card.name}, fields=["question_id", "options"])

                all_responses_match = True

                # Check if each entry in User Response Table is present in Score Card Table
                for user_response in self.response:
                    user_response_question_id = user_response.question_id
                    user_response_option = option_map.get(int(user_response.user_response_option))

                    entry_match_found = any(
                        user_response_question_id == score_card_entry.question_id and user_response_option == score_card_entry.options
                        for score_card_entry in score_card_table_entries
                    )

                    if not entry_match_found:
                        all_responses_match = False
                        break

                # If all user responses match the score card entries, append matching entries
                if all_responses_match:
                    match_found = True
                    for user_response in self.response:
                        user_response_question_id = user_response.question_id
                        user_response_option = option_map.get(int(user_response.user_response_option))
                        
                        for score_card_entry in score_card_table_entries:
                            if user_response_question_id == score_card_entry.question_id and user_response_option == score_card_entry.options:
                                self.append("score_card_table", {
                                    "question_id": user_response_question_id,
                                    "options": user_response_option,
                                    "marks": user_response.marks
                                })
                                self.review_statement = score_card.review_statement
                    frappe.msgprint("All entries in User Response Table match with Score Card Table.")
                    break

            if not match_found:
                frappe.throw("No matching entries found for all user responses in any score card.")

