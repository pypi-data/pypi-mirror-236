import React
from browser import document
import "index.css"
import "app.css"

def App(props):

    return  <div className="App">
                <header className="App-header">
                    <div className="frame">
                        <img src="react-rings-gradient.svg" className="App-logo" alt="logo" />
                    </div>
                        <p>
                            Edit <code>{" src/main.pyx "}</code> and save to reload.
                        </p>
                    <a
                        className="App-link"
                        href="https://github.com/RudreshVeerkhare/React"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Explore React
                    </a>
                </header>
            </div>


element = <App/>
print(element)
React.render(element, document.getElementById("root"))