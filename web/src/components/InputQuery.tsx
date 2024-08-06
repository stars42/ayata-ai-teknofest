import { useState } from "react";
import powerSvg from "../assets/power.svg";
import { Input } from "@headlessui/react";

const InputQuery = () => {
  const [query, setQuery] = useState("");

  const handleRun = () => {
    if (!query || query.trim() === "") {
      return;
    }

    console.log("Running query: ", query);
  };

  return (
    <div className="flex items-center justify-center w-4/5">
      <Input
        type="text"
        placeholder="Enter query..."
        className="w-3/4 p-2 border border-gray-300 rounded"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") {
            handleRun();
          }
        }}
      />
      <div className="ml-2">
        <button
          className="flex items-center p-2 border border-gray-300 rounded"
          onClick={() => handleRun()}
        >
          <img src={powerSvg} alt="Run" className="w-4 h-4 mr-2" />
          Run
        </button>
      </div>
    </div>
  );
};

export default InputQuery;
