let pass = true ;
let myprom= new promise((reject,resolve) => 
{
    if( pass = true )
    {
        resolve("Promise resolved successfully");
    }else
    {
        reject("Promise rejected");
    }
    
})
myprom.then((message) => {
    console.log(message);
}).catch((message) => {
    console.log(message);
})