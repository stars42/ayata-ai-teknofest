import { useState } from "react";
import { Switch } from "@headlessui/react";

import PowerSvg from "./assets/power.svg";
import CheckSvg from "./assets/check.svg";

import axios from "axios";
import Loader from "./components/Loader";

const API_HOST = "http://localhost:5000/api/predict";

export default function App() {
  const [inputValue, setInputValue] = useState("");
  const [isAdvancedMode, setIsAdvancedMode] = useState(false);
  const [buttonDisabled, setDisabled] = useState(false);
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleRun = () => {
    if (!inputValue || inputValue.trim() === "") {
      return;
    }

    setData([]);
    setLoading(true);
    setError(null);

    setDisabled(true);

    axios
      .post(API_HOST, {
        query: inputValue,
      })
      .then((response) => {
        console.log(response.data); // query yerine response.data olmalı
        setLoading(false);
        if (response.data.error) {
          setError(response.data.error);
          setDisabled(false);
          return;
        }
        setData(response.data);
        setDisabled(false);
      })
      .catch((error) => {
        setLoading(false);
        setError(error.response ? error.response.data : error);
        setDisabled(false);
      });
  };

  return (
    <div className="flex h-screen overflow-hidden">
      <div
        className={`w-2/5 p-4 flex flex-col justify-start items-start transition-all duration-300 ${
          isAdvancedMode ? "overflow-y-auto" : ""
        }`}
      >
        <div className="flex flex-col w-full mb-4">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            className="border p-2 w-full mb-4 border-gray-400 rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Enter query"
          />
          <div className="flex flex-row space-x-4">
            <button
              onClick={handleRun}
              className="bg-blue-500 text-white px-4 py-2 rounded mb-4 flex items-center justify-center w-1/2"
              disabled={buttonDisabled}
            >
              <img src={PowerSvg} alt="Run" className="w-4 h-4 mr-2" />
              Run
            </button>
            <button
              onClick={handleRun}
              className="bg-blue-500 text-white px-4 py-2 rounded mb-4 flex items-center justify-center w-1/2"
              disabled={buttonDisabled}
            >
              <img src={CheckSvg} alt="Run" className="w-4 h-4 mr-2" />
              Test
            </button>
          </div>
        </div>
        <div className="flex items-center mb-4">
          <Switch
            checked={isAdvancedMode}
            onChange={setIsAdvancedMode}
            className={`${
              isAdvancedMode ? "bg-blue-600" : "bg-gray-200"
            } relative inline-flex items-center h-6 rounded-full w-11`}
          >
            <span
              className={`${
                isAdvancedMode ? "translate-x-6" : "translate-x-1"
              } inline-block w-4 h-4 transform bg-white rounded-full`}
            />
          </Switch>
          <span className="ml-2">Advanced Mode</span>
        </div>
        {isAdvancedMode && (
          <div className="w-full">
            <button className="bg-gray-500 text-white px-4 py-2 rounded mb-2 w-full">
              Button 1
            </button>
            <button className="bg-gray-500 text-white px-4 py-2 rounded mb-2 w-full">
              Button 2
            </button>
          </div>
        )}
      </div>
      <div className="flex-1 p-4 border-l overflow-auto">
        <h2 className="text-xl font-bold mb-4">Output</h2>
        <div className="border p-4 h-full">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <Loader />
            </div>
          ) : error ? (
            <div className="flex items-center justify-center h-full">
              <span className="text-red-500 text-3xl">{error.message}</span>
            </div>
          ) : (
            data && <div className="text-sm">{JSON.stringify(data, null, 2)}</div>
          )}
        </div>
      </div>
    </div>
  );
}6