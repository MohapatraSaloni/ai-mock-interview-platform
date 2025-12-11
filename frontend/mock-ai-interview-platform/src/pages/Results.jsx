import { useNavigate } from "react-router-dom";

function Results({ role, finalReport }) {
  const navigate = useNavigate();

  if (!finalReport) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-slate-900">
        <div className="bg-slate-800 p-6 rounded-xl text-center text-white">
          <p>No final report available.</p>
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

  const overall = finalReport.overall_scores || {};

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900">
      <div className="bg-slate-800 p-8 rounded-xl shadow-lg w-full max-w-3xl text-white space-y-6">
        <h2 className="text-2xl font-bold">
          Interview Summary {role ? `- ${role}` : ""}
        </h2>

        <div className="bg-slate-700 p-4 rounded-md space-y-1">
          <h3 className="font-semibold mb-2">Overall Scores</h3>
          <p>Communication: {overall.communication ?? "N/A"}</p>
          <p>Technical: {overall.technical ?? "N/A"}</p>
          <p>Confidence: {overall.confidence ?? "N/A"}</p>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div className="bg-slate-700 p-4 rounded-md">
            <h3 className="font-semibold mb-2">Strengths</h3>
            <ul className="list-disc list-inside text-sm space-y-1">
              {(finalReport.strengths || []).map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>

          <div className="bg-slate-700 p-4 rounded-md">
            <h3 className="font-semibold mb-2">Weaknesses</h3>
            <ul className="list-disc list-inside text-sm space-y-1">
              {(finalReport.weaknesses || []).map((item, idx) => (
                <li key={idx}>{item}</li>
              ))}
            </ul>
          </div>
        </div>

        <div className="bg-slate-700 p-4 rounded-md">
          <h3 className="font-semibold mb-2">Improvement Plan</h3>
          <ul className="list-disc list-inside text-sm space-y-1">
            {(finalReport.improvement_plan || []).map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>

        <button
          className="mt-2 px-4 py-2 bg-indigo-500 rounded-md"
          onClick={() => navigate("/")}
        >
          Start New Interview
        </button>
      </div>
    </div>
  );
}

export default Results;
