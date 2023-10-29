import { FiSearch } from 'react-icons/fi';
import './styles.css';
import { useState } from 'react';
import { getBookRecommendation } from '../Model/getBookRecommendation';
import { currentReading } from '../Model/currentReading';
import { Oval } from 'react-loader-spinner'
import Dialog from '@mui/material/Dialog';
import { DialogTitle, DialogContent, DialogActions, Button } from '@mui/material';
import { alreadyReading } from '../Model/alreadyRead';
import { wantToRead } from '../Model/wantToRead';

export default function Home() {
    const [searchResults, setSearchResults] = useState([]);
    const [prompt, setPrompt] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(false);
    const [errorMessage, setErrorMessage] = useState("")
    const [openCurrentReadingDialog, setOpenCurrentReading] = useState(false);
    const [openAlreadyReading, setOpenAlreadyReading] = useState(false);
    const [openWantToRead, setWantToRead] = useState(false);
    const [olan, setOlan] = useState("")

    function handleShowSummary(i) {
        const newSearchResults = searchResults.slice()
        newSearchResults[i].showSummary = !newSearchResults[i].showSummary;
        setSearchResults(newSearchResults)
    }

    async function handleSubmit(event) {
        event.preventDefault();
        console.log("Clicked")
        try {
            setLoading(true);
            let response = await getBookRecommendation(prompt);
            setLoading(false);
            setSearchResults(response)
        } catch (err) {
            console.log("OH SHIT!")
            setLoading(false);
            setError(true);
            console.log(`The error is ${err}`)
            setErrorMessage(err.message)
        }
    }

    async function handleCurrentReading() {
        console.log("Clicked")
        try {
            setOpenCurrentReading(false)
            setLoading(true);
            let response = await currentReading(olan);
            setLoading(false);
            setSearchResults(response)
        } catch (err) {
            console.log("OH SHIT!")
            setLoading(false);
            setError(true);
            console.log(`The error is ${err}`)
            setErrorMessage(err.message)
        }
    }

    async function handleAlreadyReading() {
        console.log("Clicked")
        try {
            setOpenAlreadyReading(false)
            setLoading(true);
            let response = await alreadyReading(olan);
            setLoading(false);
            setSearchResults(response)
        } catch (err) {
            console.log("OH SHIT!")
            setLoading(false);
            setError(true);
            console.log(`The error is ${err}`)
            setErrorMessage(err.message)
        }
    }

    async function handleWantToRead() {
        console.log("Clicked")
        try {
            setWantToRead(false)
            setLoading(true);
            let response = await wantToRead(olan);
            setLoading(false);
            setSearchResults(response)
        } catch (err) {
            console.log("OH SHIT!")
            setLoading(false);
            setError(true);
            console.log(`The error is ${err}`)
            setErrorMessage(err.message)
        }
    }

    if (loading === true) {
        return (
            <div>
                <Oval
                    height={200}
                    width={200}
                    color="#4fa94d"
                    wrapperStyle={{}}
                    wrapperClass=""
                    visible={true}
                    ariaLabel='oval-loading'
                    secondaryColor="#4fa94d"
                    strokeWidth={2}
                    strokeWidthSecondary={2}

                />
                <p>Books Are Loading</p>
            </div>
        );
    } else if (error === true) {
        return (
            <div>
                <h2>Error Occured</h2>
                <p>{errorMessage}</p>
            </div>
        );
    } else {
        return (
            <div className='content-page'>
                {/* Search Bar */}
                <section className='search-bar'>
                    <form onSubmit={handleSubmit}>
                        <input
                            type="text"
                            placeholder="I want books on..."
                            className='search-text-field'
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                        />
                        <button type="submit" className='search-button'><FiSearch /></button>
                    </form>
                </section>
                {/* Open Library Search Suggestions */}
                <section className='open-library-search'>
                    <p>Search for books based on your OpenLibrary reading log:</p>
                    <div className='open-library-search-buttons'>
                        <MyButton
                            text={"Currently Reading"}
                            handleClick={() => setOpenCurrentReading(true)}
                        />
                        <MyButton
                            text={"Want to Read"}
                            handleClick={() => setWantToRead(true)}
                        />
                        <MyButton
                            text={"Already Read"}
                            handleClick={() => setOpenAlreadyReading(true)}
                        />
                    </div>
                </section>
                {/* Diaolog */}
                <Dialog
                    open={openCurrentReadingDialog}
                >
                    <DialogTitle>
                        Enter Your Open Library Account Details
                    </DialogTitle>
                    <DialogContent>
                        <input
                            type="text"
                            placeholder="Enter open library account name"
                            value={olan}
                            onChange={(e) => setOlan(e.target.value)}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleCurrentReading}>
                            Submit
                        </Button>
                    </DialogActions>
                </Dialog>
                <Dialog
                    open={openAlreadyReading}
                >
                    <DialogTitle>
                        Enter Your Open Library Account Details
                    </DialogTitle>
                    <DialogContent>
                        <input
                            type="text"
                            placeholder="Enter open library account name"
                            value={olan}
                            onChange={(e) => setOlan(e.target.value)}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleAlreadyReading}>
                            Submit
                        </Button>
                    </DialogActions>
                </Dialog>
                <Dialog
                    open={openWantToRead}
                >
                    <DialogTitle>
                        Enter Your Open Library Account Details
                    </DialogTitle>
                    <DialogContent>
                        <input
                            type="text"
                            placeholder="Enter open library account name"
                            value={olan}
                            onChange={(e) => setOlan(e.target.value)}
                        />
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleWantToRead}>
                            Submit
                        </Button>
                    </DialogActions>
                </Dialog>
                {/* Search Results */}
                <section className='search-results'>
                    <h2>Search Results</h2>

                    {searchResults.map((val, index) => {
                        return <SearchResult
                            key={index}
                            title={val.title}
                            author={val.author}
                            rating={val.rating}
                            description={val.description}
                            imageUrl={val.image}
                            showSummary={val.showSummary}
                            summary={val.summary}
                            moreInfoLink={`https://openlibrary.org/isbn/${val.isbn}`}
                            handleShowSummary={() => handleShowSummary(index)}
                        />
                    })}
                </section>
            </div>
        );
    }
}

function SearchResult(props) {
    if (props.showSummary === true) {
        return (
            <div className='search-result-with-summary'>
                <div className='search-result-row'>
                    <img className='search-image' src={props.imageUrl}></img>
                    <p style={{ flex: 2 }}>{props.title}</p>
                    <p style={{ flex: 2 }}>{props.author}</p>
                    <p style={{ flex: 1 }}>{props.rating}</p>
                    <p style={{ flex: 3 }}>{props.description}</p>
                    <MyButton text={'Summary'} handleClick={props.handleShowSummary} />
                    <MyButton text={'More Info'}
                        handleClick={() => {
                            window.open(props.moreInfoLink, "_blank")
                        }}
                    />
                </div>
                <p>{props.summary}</p>
            </div>
        );
    }
    return (
        <div className='search-result'>
            <img className='search-image' src={props.imageUrl}></img>
            <p style={{ flex: 2 }}>{props.title}</p>
            <p style={{ flex: 2 }}>{props.author}</p>
            <p style={{ flex: 1 }}>{props.rating}</p>
            <p style={{ flex: 3 }}>{props.description}</p>
            <MyButton text={'Summary'} handleClick={props.handleShowSummary} />
            <MyButton text={'More Info'}
                handleClick={() => {
                    window.open(props.moreInfoLink, "_blank")
                }}
            />
        </div>
    );
}

export function MyButton(props) {
    if (props.delete === true) {
        return (
            <button className='linkbox-delete' onClick={props.handleClick}>{props.text}</button>
        );
    }
    return (
        <button className='linkbox' onClick={props.handleClick}>{props.text}</button>
    );
}