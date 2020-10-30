// lib/app.ts

import * as mongoose from "mongoose";

class App {

    ...
    public mongoUrl: string = 'mongodb://localhost/CRMdb';

    constructor() {
        ...
        this.mongoSetup();
    }

    private mongoSetup(): void{
        mongoose.Promise = global.Promise;
        mongoose.connect(this.mongoUrl);
    }

}

export default new App().app;
