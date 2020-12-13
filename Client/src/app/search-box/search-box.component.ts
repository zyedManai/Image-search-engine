import { Component, OnInit } from '@angular/core';
import { HttpClient} from '@angular/common/http' 
import { ImagesService } from '../services/images.service'

@Component({
  selector: 'app-search-box',
  templateUrl: './search-box.component.html',
  styleUrls: ['./search-box.component.css']
})
export class SearchBoxComponent implements OnInit {
  selectedFile: File = null
  
  constructor(private http: HttpClient,private imagesService: ImagesService) { }

  ngOnInit(): void {
  }

  onFileSelected(event){
    this.selectedFile = <File>event.target.files[0]
    console.log(this.selectedFile)
  }
  
  onUpload(){
    //this.imagesService.images = []
    const fd = new FormData();
    fd.append('image', this.selectedFile, this.selectedFile.name)
    //this.imagesService.images = []
    this.http.post("http://127.0.0.1:5000/search",fd)
    .subscribe(
      res => {
        //this.imagesService.images= []
        for (let key in res){

          this.imagesService.images.push("../assets"+res[key][1].substring(2))
        }
        this.imagesService.images.forEach( str => {
          console.log(str)
        })
      }
    );
  }
}
