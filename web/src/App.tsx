import { ThemeProvider, useTheme } from "./contexts/ThemeProvider";
import { Switch } from "@headlessui/react";
import { useState } from "react";

function App() {
  const [query, setQuery] = useState("");
  const { theme, toggleTheme } = useTheme() as { theme: string, toggleTheme: () => void };

  return (
    <div className={`flex items-center justify-center h-screen ${getThemeClasses(theme, ['bg'])}-100`}>
      <div className="p-8 bg-white rounded-lg shadow-lg w-4/5">
        <div className="mt-4 flex items-center justify-between">
          <input
            className={`w-4/5 px-4 py-2 border rounded-md ${getThemeClasses(theme, ['border'])}-300 focus:outline-none focus:ring-2 ${getThemeClasses(theme, ['focus:ring'])}-500 focus:border-transparent`}
            placeholder="Enter query"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <span>Advanced Mode</span>
          <Switch
            checked={theme === "blue"}
            onChange={toggleTheme}
            className={`relative inline-flex items-center h-6 rounded-full w-11 ${getThemeClasses(theme, ['bg'])}-600`}
          >
            <span className="sr-only">Enable advanced mode</span>
            <span className={`inline-block w-4 h-4 transform bg-white rounded-full ${theme === "blue" ? "translate-x-6" : "translate-x-1"}`} />
          </Switch>
        </div>
      </div>
    </div>
  );
}

function getThemeClasses(theme: string, classNames: string[]) {
  return classNames.map(className => `${className}-${theme}`).join(' ');
}

export default function RootApp() {
  return (
    <ThemeProvider>
      <App />
    </ThemeProvider>
  );
}
