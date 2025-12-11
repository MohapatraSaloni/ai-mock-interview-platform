import { useState } from "react";
import { useNavigate } from "react-router-dom";

function Interview({ role, question, lastScores, onSubmitAnswer, onEndInterview }) {
  const [answer, setAnswer] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const navigate = useNavigate();

  if (!role || !question) {
    // If user refreshed the page and lost state
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="bg-slate-800 p-6 rounded-xl text-center text-white">
          <p>No active interview session.</p>
          <button
            className="mt-4 px-4 py-2 bg-indigo-500 rounded-md"
            onClick={() => navigate("/")}
          >
            Go Back Home
          </button>
        </div>
      </div>
    );
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!answer.trim()) {
      alert("Please type an answer.");
      return;
    }
    setIsSubmitting(true);
    await onSubmitAnswer(answer);
    setIsSubmitting(false);
    setAnswer(""); // clear textarea for next question
  };

  const handleEnd = async () => {
    await onEndInterview();
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900">
      <div className="bg-slate-800 p-8 rounded-xl shadow-lg w-full max-w-2xl space-y-6 text-white">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-bold">Role: {role}</h2>
          <button
            className="px-3 py-1 rounded-md bg-red-500 hover:bg-red-600"
            onClick={handleEnd}
          >
            End Interview
          </button>
        </div>

        <div className="bg-slate-700 p-4 rounded-md">
          <h3 className="font-semibold mb-2">Current Question:</h3>
          <p>{question}</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <textarea
            className="w-full h-32 p-3 rounded-md bg-slate-700 text-white"
            placeholder="Type your answer here..."
            value={answer}
            onChange={(e) => setAnswer(e.target.value)}
          />

          <button
            type="submit"
            disabled={isSubmitting}
            className="px-4 py-2 rounded-md bg-indigo-500 hover:bg-indigo-600 disabled:opacity-60"
          >
            {isSubmitting ? "Submitting..." : "Submit Answer"}
          </button>
        </form>

        {lastScores && (
          <div className="bg-slate-700 p-4 rounded-md space-y-2">
            <h3 className="font-semibold">Last Answer Feedback</h3>
            <p>
              <span className="font-semibold">Communication:</span>{" "}
              {lastScores.communication_score}
            </p>
            <p>
              <span className="font-semibold">Technical:</span>{" "}
              {lastScores.technical_score}
            </p>
            <p>
              <span className="font-semibold">Confidence:</span>{" "}
              {lastScores.confidence_score}
            </p>
            {lastScores.feedback && (
              <>
                <p className="text-sm mt-2">
                  <span className="font-semibold">
                    Communication feedback:
                  </span>{" "}
                  {lastScores.feedback.communication}
                </p>
                <p className="text-sm">
                  <span className="font-semibold">Technical feedback:</span>{" "}
                  {lastScores.feedback.technical}
                </p>
                <p className="text-sm">
                  <span className="font-semibold">
                    Confidence feedback:
                  </span>{" "}
                  {lastScores.feedback.confidence}
                </p>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default Interview;

