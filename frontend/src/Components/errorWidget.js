export default function ErrorWidget(props) {
    return (
        <div>
            <h2>Error Occured</h2>
            <p>{props.message}</p>
        </div>
    );
}