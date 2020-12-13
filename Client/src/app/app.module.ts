import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { ImageListComponent } from './image-list/image-list.component';
import { SearchBoxComponent } from './search-box/search-box.component';
import { HttpClientModule } from '@angular/common/http'
import { ImagesService} from "./services/images.service"

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    ImageListComponent,
    SearchBoxComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule
  ],
  providers: [ImagesService],
  bootstrap: [AppComponent]
})
export class AppModule { }
