import "./App.css";
import { useState } from "react";
import ProductCard from "./components/ProductCard";
import ProductSearch from "./components/ProductSearch";
import TwitterReport from "./components/TwitterReport";

function App() {
    const [prodDetails, setProdDetails] = useState(null);
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(false);
    return (
        <main>
            <h1 className="header">flippy</h1>
            <ProductSearch setProdDetails={setProdDetails} />
            {prodDetails && (
                <ProductCard
                    prodDetails={prodDetails}
                    setReport={setReport}
                    setLoading={setLoading}
                />
            )}
            {loading ? "Analysing social media posts..." : ""}
            {report && <TwitterReport report={report} />}
        </main>
    );
}

export default App;
