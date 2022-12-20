(define space-parent-concept
  (def-concept :name "" :is_slot True))
(define conceptual-space
  (def-conceptual-space :name "" :parent_concept space-parent-concept
    :possible_instances (StructureSet temperature-space height-space goodness-space)
    :no_of_dimensions 1))
(define label-parent-concept
  (def-concept :name "" :is_slot True :parent_space conceptual-space))
(define jj-input
  (def-contextual-space :name "ap[jj].meaning" :parent_concept input-concept
    :conceptual_spaces (StructureSet conceptual-space)))
(define jj-output
  (def-contextual-space :name "ap[jj].text" :parent_concept text-concept
    :conceptual_spaces (StructureSet grammar-space conceptual-space)))
(define jj-frame
  (def-frame :name "ap[jj]"
    :parent_concept ap-concept :parent_frame None
    :sub_frames (StructureSet)
    :concepts (StructureSet label-parent-concept)
    :input_space jj-input :output_space jj-output))
(define chunk
  (def-chunk :locations (list (Location (list (list Nan)) conceptual-space)
			      (Location (list) jj-input))
    :parent_space jj-input))
(setattr jj-frame "early_chunk" chunk)
(setattr jj-frame "late_chunk" chunk)
(define chunk-label
  (def-label :start chunk :parent_concept label-parent-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) jj-input))))
(define letter-chunk
  (def-letter-chunk :name None
    :locations (list (Location (list (list Nan)) conceptual-space)
		     jj-location
		     (Location (list) jj-output))
    :parent_space jj-output))
(define letter-chunk-grammar-label
  (def-label :start letter-chunk :parent_concept jj-concept
    :locations (list jj-location
		     (Location (list) jj-output))))
(define letter-chunk-meaning-label
  (def-label :start letter-chunk :parent_concept label-parent-concept
    :locations (list (Location (list (list Nan)) conceptual-space)
		     (Location (list) jj-output))))
(define null-chunk
  (def-letter-chunk :name ""
    :locations (list null-location
		     (Location (list) jj-output))
    :parent_space jj-output))
(define ap-super-chunk
  (def-letter-chunk :name None
    :locations (list ap-location
		     (Location (list) jj-output))
    :parent_space jj-output
    :left_branch (StructureSet letter-chunk)
    :right_branch (StructureSet null-chunk)))
(define ap-super-chunk-label
  (def-label :start ap-super-chunk :parent_concept ap-concept
    :locations (list ap-location
		     (Location (list) jj-output))))

(def-relation :start temperature-concept :end jj-frame
  :is_bidirectional True :stable_activation 1.0)
(def-relation :start height-concept :end jj-frame
  :is_bidirectional True :stable_activation 1.0)
(def-relation :start goodness-concept :end jj-frame
  :is_bidirectional True :stable_activation 1.0)
