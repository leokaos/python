// file-upload.component.ts
import { ChangeDetectorRef, Component, model } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { catchError, concat, concatMap, filter, finalize, from, map, of, tap } from 'rxjs';
import { GalleriaModule } from 'primeng/galleria';

@Component({
  selector: 'app-file-upload',
  templateUrl: './file-upload.html',
  imports: [CommonModule, FormsModule, GalleriaModule],
  styleUrls: ['./file-upload.css']
})
export class FileUpload {

  selectedFiles: FileList | null = null;
  // No seu componente:
  images: any[] = [];
  galleriaInitialized = false;

  responsiveOptions: any[] = [
    {
      breakpoint: '1300px',
      numVisible: 3
    },
    {
      breakpoint: '575px',
      numVisible: 1
    }
  ];

  available_filters: string[] = [
    "_1977",
    "aden",
    "brannan",
    "brooklyn",
    "clarendon",
    /*"earlybird",
    "gingham",
    "hudson",
    "inkwell",
    "kelvin",
    "lark",
    "lofi",
    "maven",
    "mayfair",
    "moon",
    "nashville",
    "perpetua",
    "reyes",
    "rise",
    "slumber",
    "stinson",
    "toaster",
    "valencia",
    "walden",
    "willow",
    "xpro2"*/
  ]

  constructor(private http: HttpClient, private cdr: ChangeDetectorRef) { }

  onFileSelect(event: Event): void {
    const input = event.target as HTMLInputElement;
    this.selectedFiles = input.files;
  }

  uploadToSelectedEndpoint(): void {
    if (!this.selectedFiles || this.selectedFiles.length === 0) {
      return;
    }

    this.uploadFiles(this.selectedFiles!);
  }

  private uploadFiles(files: FileList): void {
    const file = files[0];
    if (!file) return;

    // 1. Reset inicial
    this.images = [];
    this.galleriaInitialized = false;
    this.cdr.detectChanges(); // Força renderização inicial

    const formData = new FormData();
    formData.append('file', file, file.name);

    from(this.available_filters).pipe(
      concatMap(filter => {
        return this.http.post(`http://localhost:8000/images/apply-filter/${filter}`, formData, {
          responseType: 'blob'
        }).pipe(
          map(blob => {
            const imageObj = {
              itemImageSrc: URL.createObjectURL(blob),
              thumbnailImageSrc: URL.createObjectURL(blob),
              filterName: filter
            };

            // 2. Adiciona cada imagem imediatamente
            this.images = [...this.images, imageObj];
            this.galleriaInitialized = true;
            this.cdr.detectChanges(); // Força atualização

            return imageObj;
          })
        );
      })
    ).subscribe();
  }

  resetSelection(): void {
    this.selectedFiles = null;
    const fileInput = document.getElementById('fileInput') as HTMLInputElement;
    if (fileInput) {
      fileInput.value = '';
    }
  }

  ngOnDestroy() {
    // Limpa as URLs para evitar vazamento de memória
    this.images.forEach(img => {
      if (img.startsWith('blob:')) {
        URL.revokeObjectURL(img);
      }
    });
  }

  ngOnInit() {
    this.images = [
      {
        itemImageSrc: 'https://primefaces.org/cdn/primeng/images/galleria/galleria1.jpg',
        thumbnailImageSrc: 'https://primefaces.org/cdn/primeng/images/galleria/galleria1s.jpg',
        filterName: 'teste'
      }
    ];
    this.cdr.detectChanges();
  }
}