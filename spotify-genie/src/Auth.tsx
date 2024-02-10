import React, { useEffect, useState } from "react";

export default function Auth() {
    const [num, setNum] = useState();
    useEffect(() => {
        const fetchNum = async () => {
            const res = await fetch('/spotify');
            const data = await res.json();
            console.log(data)
            setNum(data.number)
        }
        fetchNum();
    }, [])
    return <div><h3>Hello This is a test. And this is the data from spotify link {num}</h3></div>
}
