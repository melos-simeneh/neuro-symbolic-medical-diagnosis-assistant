import { useState } from "react";
import {
  FaSpinner,
  FaStethoscope,
  FaInfoCircle,
  FaCheckCircle,
  FaClinicMedical,
} from "react-icons/fa";
import { GiHealthNormal } from "react-icons/gi";

export default function DiagnosisForm() {
  const [patientName, setPatientName] = useState("");
  const [symptoms, setSymptoms] = useState("");
  const [diagnosisResult, setDiagnosisResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleNameChange = (e) => {
    const value = e.target.value;
    const filteredValue = value.replace(/[^a-zA-Z'-]/g, "");
    setPatientName(filteredValue);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setDiagnosisResult(null);

    try {
      const response = await fetch("http://localhost:3000/diagnosis", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          patient_name: patientName,
          raw_symptoms: symptoms,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        const errorMessage =
          data?.message || `[Error]: HTTP error! status: ${response.status}`;
        throw new Error(errorMessage);
      }

      setDiagnosisResult(data);
    } catch (err) {
      setError(err.message);
      console.error("[Error]: unable to submit request", err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-3xl min-w-3xl mx-auto my-8 p-10 px-16 rounded-2xl bg-white shadow-lg">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-gray-700 mb-2 flex items-center justify-center">
          <GiHealthNormal className="mr-3 text-blue-500" />
          Medical Diagnosis Assistant
        </h2>
        <p className="text-gray-600">
          Please provide a detailed description of your symptoms to receive an
          initial medical evaluation.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Patient Name Field */}
        <div className="form-group">
          <label className="block text-sm font-medium text-gray-700 mb-1">
            First Name
          </label>
          <div className="relative">
            <input
              type="text"
              value={patientName}
              onChange={handleNameChange}
              className={`w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all`}
              placeholder="Enter your first name"
              required
              pattern="[a-zA-Z'-]+"
              title="Please enter only your first name (letters only)"
            />
          </div>
        </div>

        {/* Symptoms Fields */}
        <div className="form-group">
          <div className="mb-4">
            <label
              htmlFor="symptoms"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Describe your symptoms
            </label>
            <textarea
              id="symptoms"
              name="symptoms"
              value={symptoms}
              onChange={(e) => setSymptoms(e.target.value)}
              className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
              placeholder="Please describe your symptoms in detail here..."
              rows={4}
              required
            />
          </div>
        </div>

        {/* Submit Button */}
        <div className="pt-4">
          <button
            type="submit"
            className="w-full py-3 px-6 bg-gradient-to-r from-blue-600 to-teal-500 hover:from-blue-700 hover:to-teal-600 text-white font-medium rounded-lg shadow-md hover:shadow-lg transition-all duration-300 flex justify-center items-center"
            disabled={isLoading}
          >
            {isLoading ? (
              <>
                <FaSpinner className="animate-spin mr-3 h-5 w-5 text-white" />
                Analyzing Symptoms...
              </>
            ) : (
              <>
                <FaStethoscope className="h-5 w-5 mr-2" />
                Get Diagnosis
              </>
            )}
          </button>
        </div>
      </form>

      {/* Error Message */}
      {error && (
        <div className="mt-6 p-4 bg-red-50 rounded-lg border border-red-200">
          <div className="flex items-center text-red-600">
            <FaInfoCircle className="mr-2" />
            <span>[Error]: {error}</span>
          </div>
        </div>
      )}

      {/* Diagnosis Results */}
      {diagnosisResult && !error && (
        <div className="mt-10 p-6 bg-gradient-to-br from-blue-50 to-teal-50 rounded-xl border border-blue-100 shadow-sm">
          <div className="flex items-center mb-4">
            <FaInfoCircle className="h-8 w-8 text-blue-600 mr-3" />
            <h3 className="text-2xl font-bold text-gray-800">
              Diagnosis Results for {diagnosisResult.patient_name}
            </h3>
          </div>

          <div className="space-y-4">
            {/* Extracted Symptoms Section */}
            <div className="p-4 bg-white rounded-lg shadow-xs">
              <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                <FaClinicMedical className="h-5 w-5 text-blue-500 mr-2" />
                Extracted Symptoms:
              </h4>
              <ul className="space-y-1 pl-2">
                {diagnosisResult.symptoms.map((symptom, i) => (
                  <li
                    key={i}
                    className="flex items-start text-gray-700 before:content-['•'] before:mr-2 before:text-blue-500"
                  >
                    {symptom}
                  </li>
                ))}
              </ul>
            </div>

            {/* Possible Conditions Section */}
            <div className="p-4 bg-white rounded-lg shadow-xs">
              {diagnosisResult.diagnosis_result.length > 0 ? (
                <>
                  <h4 className="font-semibold text-gray-700 mb-3 flex items-center">
                    <FaCheckCircle className="h-5 w-5 text-teal-500 mr-2" />
                    Possible Conditions:
                  </h4>
                  <ul className="space-y-2 pl-2">
                    {diagnosisResult.diagnosis_result.map((condition, i) => (
                      <li
                        key={i}
                        className="flex items-start text-gray-700 before:content-['•'] before:mr-2 before:text-teal-500"
                      >
                        {condition}
                      </li>
                    ))}
                  </ul>

                  {/* Disclaimer Note - Only shown when there are diagnosis results */}
                  <div className="mt-5 p-4 bg-blue-50 rounded-lg border border-blue-100">
                    <div className="flex">
                      <FaInfoCircle className="h-5 w-5 text-blue-500 mr-2 mt-0.5" />
                      <p className="text-sm text-blue-700">
                        <strong>Note:</strong> This is a preliminary assessment.
                        For serious symptoms or if symptoms persist, please
                        consult a healthcare professional.
                      </p>
                    </div>
                  </div>
                </>
              ) : (
                <p className="text-amber-600 font-medium bg-amber-50 px-3 py-2 rounded-md border border-amber-100 flex items-start">
                  <FaInfoCircle className="mr-2 mt-0.5 flex-shrink-0" />I am
                  unable to make a diagnosis. Please provide more detailed
                  symptom descriptions.
                </p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
