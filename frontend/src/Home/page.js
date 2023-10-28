import { FiSearch } from 'react-icons/fi';
import './styles.css';
import { useState } from 'react';
import { getBookRecommendation } from '../Model/getBookRecommendation';

export default function Home() {
    const [searchResults, setSearchResults] = useState([
        {
            showSummary: false,
            description: "Harry Potter and the Philosopher's Stone is a fantasy novel written by British author J. K. Rowling",
            title: "Harry Potter and the Sorcerer's Stone",
            author: "J. K. Rowling",
            rating: 4.6,
            summary: "The book is about 11 year old Harry Potter, who receives a letter saying that he is invited to attend Hogwarts, school of witchcraft and wizardry. He then learns that a powerful wizard and his minions are after the sorcerer's stone that will make this evil wizard immortal and undefeatable.",
            imageUrl: "https://covers.openlibrary.org/b/id/13741661-M.jpg",
            moreInfoLink: "https://openlibrary.org/works/OL34924410W/Harry_Potter_And_The_Sorcer%27s_Stone?edition=key%3A/books/OL7893441M"
        }
    ]);
    const [prompt, setPrompt] = useState("");

    function handleShowSummary(i) {
        const newSearchResults = searchResults.slice()
        newSearchResults[i].showSummary = !newSearchResults[i].showSummary;
        setSearchResults(newSearchResults)
    }

    async function handleSubmit(event) {
        event.preventDefault();
        console.log("Clicked")
        try {
            let response = await getBookRecommendation(prompt);
            setSearchResults(response)
        } catch(err) {
            console.log("OH SHIT!")
        }
    }

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
                        handleClick={() => console.log("Currently Reading clicked")}
                    />
                    <MyButton 
                        text={"Want to Read"}
                        handleClick={() => console.log("Want to Read clicked")}
                    />
                    <MyButton 
                        text={"Already Read"}
                        handleClick={() => console.log("Already Read clicked")}
                    />
                </div>
            </section>
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
                        imageUrl={val.imageUrl}
                        showSummary={val.showSummary}
                        summary={val.summary}
                        moreInfoLink={val.moreInfoLink}
                        handleShowSummary={() => handleShowSummary(index)}
                    />
                })}
            </section>
        </div>
    );
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
    if(props.delete === true) {
        return (
            <button className='linkbox-delete' onClick={props.handleClick}>{props.text}</button>
        );
    }
    return (
        <button className='linkbox' onClick={props.handleClick}>{props.text}</button>
    );
}