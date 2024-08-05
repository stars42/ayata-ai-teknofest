import { Switch } from "@headlessui/react";
import { useState } from "react";

const AdvancedMenu = () => {
  const [advancedMode, setAdvancedMode] = useState(false);

  return (
    <div className="flex items-left mt-4">
      <Switch
        checked={advancedMode}
        onChange={setAdvancedMode}
        className={`${
          advancedMode ? "bg-blue-600" : "bg-gray-200"
        } relative inline-flex items-center h-6 rounded-full w-11`}
      >
        <span className="sr-only">Enable advanced mode</span>
        <span
          className={`${
            advancedMode ? "translate-x-6" : "translate-x-1"
          } inline-block w-4 h-4 transform bg-white rounded-full`}
        />
      </Switch>
      <span className="ml-2">Advanced mode</span>
    </div>
  );
};

export default AdvancedMenu;
