import { Routes, Route, Link, useNavigate } from "react-router-dom";
import { useState } from "react";

import RoleSelection from "./pages/RoleSelection";
import Interview from "./pages/Interview";
import Results from "./pages/Results";
import { API_BASE_URL } from "./apiConfig";

const MAX_QUESTIONS = 10;

function App() {
  const [role, setRole] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [currentQuestion, setCurrentQuestion] = useState("");
  const [lastScores, setLastScores] = useState(null);
  const [finalReport, setFinalReport] = useState(null);
  const [questionCount, setQuestionCount] = useState(0); // how many questions have been asked

  const navigate = useNavigate();

  // ---- API CALL: start-interview ----
  const startInterview = async (selectedRole) => {
    try {
      const res = await fetch(`${API_BASE_URL}/start-interview`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          role: selectedRole,
          user_id: "demo-user-1", // later you can make this dynamic
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to start interview");
      }

      const data = await res.json();
      setRole(selectedRole);
      setSessionId(data.session_id);
      setCurrentQuestion(data.question);
      setLastScores(null);
      setFinalReport(null);
      setQuestionCount(1); // first question has been asked

      navigate("/interview");
    } catch (err) {
      console.error(err);
      alert("Error starting interview. Check backend and console.");
    }
  };

  // ---- API CALL: final-feedback ----
  const getFinalFeedback = async () => {
    if (!sessionId || !role) {
      alert("No active session.");
      return;
    }

    try {
      const res = await fetch(`${API_BASE_URL}/final-feedback`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          role,
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to get final feedback");
      }

      const data = await res.json();
      setFinalReport(data);
      navigate("/results");
    } catch (err) {
      console.error(err);
      alert("Error getting final feedback. Check backend and console.");
    }
  };

  // ---- API CALL: submit-answer ----
  const submitAnswer = async (answerText) => {
    if (!sessionId || !role || !currentQuestion) {
      alert("Missing interview session info.");
      return;
    }

    try {
      const res = await fetch(`${API_BASE_URL}/submit-answer`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          role,
          question: currentQuestion,
          answer: answerText,
        }),
      });

      if (!res.ok) {
        throw new Error("Failed to submit answer");
      }

      const data = await res.json();
      setLastScores(data.scores);

      // We have just answered question #questionCount
      // If this was question 10 (MAX_QUESTIONS), end the interview
      if (questionCount >= MAX_QUESTIONS) {
        await getFinalFeedback();
      } else {
        // Otherwise move to next question
        setCurrentQuestion(data.next_question);
        setQuestionCount((prev) => prev + 1);
      }
    } catch (err) {
      console.error(err);
      alert("Error submitting answer. Check backend and console.");
    }
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white">
      {/* simple nav for debugging, can hide later */}
      <nav className="p-4 bg-slate-800 flex gap-4">
        <Link to="/">Home</Link>
        <Link to="/interview">Interview</Link>
        <Link to="/results">Results</Link>
      </nav>

      <Routes>
        <Route
          path="/"
          element={<RoleSelection onStartInterview={startInterview} />}
        />
        <Route
          path="/interview"
          element={
            <Interview
              role={role}
              question={currentQuestion}
              lastScores={lastScores}
              questionCount={questionCount}
              maxQuestions={MAX_QUESTIONS}
              onSubmitAnswer={submitAnswer}
              onEndInterview={getFinalFeedback}
            />
          }
        />
        <Route
          path="/results"
          element={<Results role={role} finalReport={finalReport} />}
        />
      </Routes>
    </div>
  );
}

export default App;
