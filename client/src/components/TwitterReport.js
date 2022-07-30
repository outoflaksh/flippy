import React from "react";

const TwitterReport = ({ report, loading }) => {
    return (
        <div className="report-container">
            <div className="col">
                <section>
                    <h4 className="sec-heading">Social media report:</h4>
                    <h1>Total posts analysed: {report.total_tweets}</h1>
                </section>
                <section>
                    <h4 className="sec-heading">Breakdown:</h4>
                    <h1>Positive posts: {report.breakdown.positive}</h1>
                    <h1>Neutral posts: {report.breakdown.neutral}</h1>
                    <h1>Negative posts: {report.breakdown.negative}</h1>
                </section>
            </div>
            <div className="col">
                <section>
                    <h4 className="sec-heading">Score:</h4>
                    <h1>{report.score}/10</h1>
                </section>
                <section>
                    <h4 className="sec-heading">General consensus:</h4>
                    <h1>{report.net_result[0]}</h1>
                </section>
            </div>
        </div>
    );
};

export default TwitterReport;
