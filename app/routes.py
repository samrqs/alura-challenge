import json

from flask import render_template
from collections import Counter
from app.models import Feedback, Classification
from .extensions import db

from flask import Blueprint
from flask import request, jsonify
from classifier import sentiment_classifier

main_bp = Blueprint("main", __name__)

@main_bp.route("/feedbacks", methods=["POST"])
def classifier():
    data = request.json
    feedback = data.get("feedback")

    if not feedback:
        return jsonify({"erro": "Feedback is required"}), 400
    
    novo_feedback = Feedback(
        feedback_text=feedback,
    )
    
    db.session.add(novo_feedback)
    db.session.commit()

    result = json.loads(sentiment_classifier(feedback))

    sentiment = result.get("sentiment")
    features = result.get("requested_features", [])

    classifications = []
    for feature in features:
        classification = Classification(
            sentiment=sentiment,
            code=feature["code"],
            reason=feature["reason"],
            feedbacks_id=novo_feedback.id
        )
        db.session.add(classification)
        classifications.append(classification)

    db.session.commit()

    return jsonify({
        "feedback_id": str(novo_feedback.id),
        "sentiment": sentiment,
        "requested_features": [
            {
                "code": classification.code,
                "reason": classification.reason
            } 
        ]
    }), 201


@main_bp.route("/relatorio", methods=["GET"])
def relatorio():
     
    feedbacks = Feedback.query.all()

    data = []

    total_feedbacks = len(feedbacks)

    positives = 0
    all_codes = []

    for feedback in feedbacks:
        classification = Classification.query.filter_by(feedbacks_id=feedback.id).all()

        sentiments = set(cls.sentiment for cls in classification)

        if 'POSITIVO' in sentiments:
            positives += 1

        for cls in classification:
            all_codes.append(cls.code)

        data.append({
            "feedback": feedback.feedback_text,
            "classificacoes": [
                {
                    "sentiment": cls.sentiment,
                    "code": cls.code,
                    "reason": cls.reason
                } for cls in classification
            ]
        })

    positives_percent = round((positives / total_feedbacks) * 100, 2) if total_feedbacks else 0
    most_mentioned = Counter(all_codes).most_common(5)  # top 5 features

    return render_template("relatorio.html", feedbacks=data,
        positives_percent=positives_percent, most_mentioned=most_mentioned)