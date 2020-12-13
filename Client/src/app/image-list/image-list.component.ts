import { Component, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { ImagesService } from '../services/images.service'

@Component({
  selector: 'app-image-list',
  templateUrl: './image-list.component.html',
  styleUrls: ['./image-list.component.css']
})
export class ImageListComponent implements OnInit, OnChanges {

  images = []
  constructor(private imagesService: ImagesService) { 

  }
  ngOnChanges(changes: SimpleChanges): void {
    //this.images = this.imagesService.getImages();
    //console.log("Changed"); 
  }

  ngOnInit(): void {
    this.images = this.imagesService.getImages();
    console.log("Changed"); 
  }

}
