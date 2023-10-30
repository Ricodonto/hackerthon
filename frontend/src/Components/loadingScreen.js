import { Oval } from 'react-loader-spinner'

export default function LoadingScreen(props) {
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
            <p>{props.message}</p>
        </div>
    );
}