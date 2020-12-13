import { HttpClient } from '@angular/common/http'
import {Injectable} from "@angular/core"

@Injectable()
export class ImagesService {

    images = []

    constructor(private httpClient: HttpClient){
        
    }

    getImages(){
        return this.images;
    }


}