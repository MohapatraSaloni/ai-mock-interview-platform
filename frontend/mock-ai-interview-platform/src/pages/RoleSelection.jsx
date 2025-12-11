import { useState } from "react";

function RoleSelection({ onStartInterview }) {
  const [selectedRole, setSelectedRole] = useState("Machine Learning Engineer");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!selectedRole) {
      alert("Please select a role.");
      return;
    }
    onStartInterview(selectedRole);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-900">
      <div className="bg-slate-800 p-8 rounded-xl shadow-lg w-full max-w-md">
        <h1 className="text-2xl font-bold text-white mb-4 text-center">
          AI Mock Interview
        </h1>
        <form onSubmit={handleSubmit} className="space-y-4">
          <label className="block text-slate-200">
            Select Interview Role
            <select
              className="mt-2 w-full p-2 rounded-md bg-slate-700 text-white"
              value={selectedRole}
              onChange={(e) => setSelectedRole(e.target.value)}
            >
              <option>Machine Learning Engineer</option>
              <option>Data Analyst</option>
              <option>Backend Developer</option>
              <option>Frontend Developer</option>
            </select>
          </label>

          <button
            type="submit"
            className="w-full mt-4 py-2 rounded-md bg-indigo-500 hover:bg-indigo-600 text-white font-semibold"
          >
            Start Interview
          </button>
        </form>
      </div>
    </div>
  );
}

export default RoleSelection;
